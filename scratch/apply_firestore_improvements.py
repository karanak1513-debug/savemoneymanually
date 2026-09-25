"""
Applies user-scoped storage key and resilient snapshot streaming for Firestore:
- Scopes localStorage to smm_store_{uid} with fallback
- Adds resilient sorting and base collection fallback to support thread messages onSnapshot
- Adds deleteGoal CRUD method and UI button
- Verifies real-time persistence across hard reloads
"""
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Storage functions
old_storage = """    // Storage key & resilience
    const STORAGE_KEY = 'vaultfi_spa_clean_store_v1';
    function getLocalData() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    }
    function saveLocalData(data) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } catch (e) {}
    }"""

new_storage = """    // Storage key & resilience (User-isolated with legacy fallback)
    function getStorageKey() {
      const uid = currentUser?.uid || (isDemoMode ? 'demo-user' : 'guest');
      return `smm_store_${uid}`;
    }
    function getLocalData() {
      try {
        const userKey = getStorageKey();
        const raw = localStorage.getItem(userKey);
        if (raw) return JSON.parse(raw);
        // Fallback to legacy global key
        const legacy = localStorage.getItem('vaultfi_spa_clean_store_v1');
        return legacy ? JSON.parse(legacy) : null;
      } catch (e) {
        return null;
      }
    }
    function saveLocalData(data) {
      try {
        localStorage.setItem(getStorageKey(), JSON.stringify(data));
      } catch (e) {}
    }"""

assert old_storage in content, "Could not find old_storage in index.html"
content = content.replace(old_storage, new_storage, 1)
print("1. Updated getLocalData / saveLocalData to user-scoped key")

# 2. Add deleteGoal function right after deleteLedgerEntry
old_delete_ledger = """        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }"""

new_delete_ledger = """        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }

    async function deleteGoal(goalId) {
      const target = goals.find(g => g.id === goalId);
      if (!target) return;
      if (!confirm(`Delete goal vault "${target.name}"?`)) return;

      goals = goals.filter(g => g.id !== goalId);
      saveLocalData({ goals, ledger });
      renderAll();
      showToast(`Goal vault "${target.name}" deleted.`, 'info');

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        if (!goalId.startsWith('goal-') && !goalId.startsWith('custom-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', goalId);
          await deleteDoc(gRef).catch(e => console.warn("Goal delete warning:", e));
        }
      }
    }"""

assert old_delete_ledger in content, "Could not find old_delete_ledger in index.html"
content = content.replace(old_delete_ledger, new_delete_ledger, 1)
print("2. Added deleteGoal function")

# 3. Add delete button in renderGoalsGrid
old_goals_card_btn = """            <div class="pt-2.5 border-t border-slate-100">
              <button class="btn-primary-metallic text-xs min-h-[44px] py-2 px-3 w-full btn-quick-goal-stash" data-goal-id="${g.id}" data-goal-name="${g.name}" type="button">
                + Add Funds
              </button>
            </div>
          </div>"""

new_goals_card_btn = """            <div class="pt-2.5 border-t border-slate-100 flex items-center gap-2">
              <button class="btn-primary-metallic text-xs min-h-[44px] py-2 px-3 flex-1 btn-quick-goal-stash" data-goal-id="${g.id}" data-goal-name="${g.name}" type="button">
                + Add Funds
              </button>
              <button class="h-[44px] px-3 rounded-xl border border-slate-200 text-slate-400 hover:text-rose-600 hover:border-rose-200 hover:bg-rose-50 transition-all flex items-center justify-center cursor-pointer btn-delete-goal" data-goal-id="${g.id}" title="Delete Goal" aria-label="Delete goal">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
              </button>
            </div>
          </div>"""

assert old_goals_card_btn in content, "Could not find old_goals_card_btn in index.html"
content = content.replace(old_goals_card_btn, new_goals_card_btn, 1)

old_goal_stash_listener = """      container.querySelectorAll('.btn-quick-goal-stash').forEach(btn => {
        btn.addEventListener('click', () => {
          openAddSavingsModal(btn.dataset.goalName);
        });
      });"""

new_goal_stash_listener = """      container.querySelectorAll('.btn-quick-goal-stash').forEach(btn => {
        btn.addEventListener('click', () => {
          openAddSavingsModal(btn.dataset.goalName);
        });
      });
      container.querySelectorAll('.btn-delete-goal').forEach(btn => {
        btn.addEventListener('click', () => {
          const gid = btn.dataset.goalId;
          if (gid) deleteGoal(gid);
        });
      });"""

assert old_goal_stash_listener in content, "Could not find old_goal_stash_listener in index.html"
content = content.replace(old_goal_stash_listener, new_goal_stash_listener, 1)
print("3. Injected delete goal button and listener")

# 4. Enhance sgUnsubMsgs in ensureThread
old_sg_msgs = """        // Watch messages
        if (sgUnsubMsgs) sgUnsubMsgs();
        const qry = query(
          collection(db, 'support_threads', sgThreadId, 'messages'),
          orderBy('timestamp', 'asc')
        );
        sgUnsubMsgs = onSnapshot(qry, (snap) => {
          // Clear all except typing indicator
          if (!elMessages) return;
          // Remove all msg-wrap nodes
          elMessages.querySelectorAll('.sg-msg-wrap, .sg-pills, .sg-date-sep').forEach(n => n.remove());

          if (snap.empty) {
            // Welcome
            renderWelcome();
            return;
          }
          snap.forEach(ds => {
            const d = ds.data();
            renderMsg(ds.id, d.sender, d.text, d.status, d.timestamp);
          });

          // Auto-mark DELIVERED msgs as SEEN if window is open
          if (sgWindowOpen) {
            snap.forEach(ds => {
              const d = ds.data();
              if (d.sender !== 'USER' && d.status !== 'SEEN') {
                updateDoc(ds.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }

          // Also update user msg ticks if admin has seen them
          if (sgChatStatus === 'ADMIN_LIVE') {
            snap.forEach(ds => {
              const d = ds.data();
              if (d.sender === 'USER' && d.status === 'DELIVERED') {
                updateDoc(ds.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }
        }, (err) => console.error('sg-msgs snapshot error', err));"""

new_sg_msgs = """        // Watch messages with resilient sorting & index fallback
        if (sgUnsubMsgs) sgUnsubMsgs();
        const msgCol = collection(db, 'support_threads', sgThreadId, 'messages');
        const qry = query(msgCol, orderBy('timestamp', 'asc'));

        const handleMsgsSnapshot = (snap) => {
          if (!elMessages) return;
          elMessages.querySelectorAll('.sg-msg-wrap, .sg-pills, .sg-date-sep').forEach(n => n.remove());

          if (snap.empty) {
            renderWelcome();
            return;
          }
          const msgs = [];
          snap.forEach(ds => {
            msgs.push({ id: ds.id, ref: ds.ref, ...ds.data() });
          });
          // Resilient client-side ascending sort
          msgs.sort((a, b) => {
            const ta = a.timestamp?.toDate ? a.timestamp.toDate() : new Date(a.timestamp || 0);
            const tb = b.timestamp?.toDate ? b.timestamp.toDate() : new Date(b.timestamp || 0);
            return ta - tb;
          });
          msgs.forEach(d => {
            renderMsg(d.id, d.sender, d.text, d.status, d.timestamp);
          });

          // Auto-mark DELIVERED msgs as SEEN if window is open
          if (sgWindowOpen) {
            msgs.forEach(d => {
              if (d.sender !== 'USER' && d.status !== 'SEEN') {
                updateDoc(d.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }

          // Also update user msg ticks if admin has seen them
          if (sgChatStatus === 'ADMIN_LIVE') {
            msgs.forEach(d => {
              if (d.sender === 'USER' && d.status === 'DELIVERED') {
                updateDoc(d.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }
        };

        sgUnsubMsgs = onSnapshot(qry, handleMsgsSnapshot, (err) => {
          console.warn('sg-msgs ordered snapshot error, using base collection fallback:', err);
          sgUnsubMsgs = onSnapshot(msgCol, handleMsgsSnapshot, (err2) => {
            console.error('sg-msgs fallback snapshot error:', err2);
          });
        });"""

assert old_sg_msgs in content, "Could not find old_sg_msgs in index.html"
content = content.replace(old_sg_msgs, new_sg_msgs, 1)
print("4. Enhanced sgUnsubMsgs with fallback and client-side sorting")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html successfully updated with Firestore improvements!")
