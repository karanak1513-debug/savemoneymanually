# -*- coding: utf-8 -*-
"""
Applies Realtime Client Pipeline (onSnapshot Architecture) & Atomic Firestore Sync:
1. Adds `increment` to firebase-firestore.js imports.
2. Updates `initDataSync(user)`:
   - Sets up onSnapshot on /users/{uid}/ledger with query(..., orderBy('timestamp', 'desc'))
   - In listener: recalculates net capital (ADD vs MINUS), updates #totalStashedDisplay immediately,
     re-renders ledger history cards stack and table with inline edit/delete, updates monthly savings calendar.
   - Sets up onSnapshot on /users/{uid}/goals.
   - Explicit error callbacks logging to console.error.
3. Converts persistLedgerEntry, updateLedgerEntry, deleteLedgerEntry, persistGoal to async functions.
4. Uses atomic setDoc(doc(db, 'users', uid), { totalSaved: increment(delta) }, { merge: true }).
5. Updates form submissions (Add Savings, Withdrawal, Create Goal, Edit Entry, Delete Entry) to be async,
   disabling buttons immediately (lockBtn) to prevent duplicates, and re-enabling upon promise resolution (finally).
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Firestore Imports to include increment
old_import = """      onSnapshot,
      query,
      orderBy,
      serverTimestamp
    } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";"""

new_import = """      onSnapshot,
      query,
      orderBy,
      serverTimestamp,
      increment
    } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";"""

if old_import in html:
    html = html.replace(old_import, new_import, 1)
    print("Updated Firestore imports to include increment.")
else:
    print("Warning: old_import pattern not found directly, checking...")
    if "increment" not in html:
        idx_imp = html.find('serverTimestamp')
        if idx_imp != -1:
            html = html[:idx_imp] + 'serverTimestamp,\n      increment' + html[idx_imp+len('serverTimestamp'):]
            print("Added increment to imports via fallback.")

# 2. Replace initDataSync, persistGoal, persistLedgerEntry, updateLedgerEntry, deleteLedgerEntry
old_sync_start = html.find('// ============================================================')
old_sync_start = html.find('// DATA PERSISTENCE & REAL-TIME FIRESTORE SYNC', old_sync_start)
old_sync_end = html.find('// ============================================================', old_sync_start)
old_sync_end = html.find('// RENDERING ENGINES ACROSS ALL 4 CORE VIEWS', old_sync_end)
# We want to replace from before old_sync_start up to old_sync_end

# Let's locate the comment header
marker_start = "    // ============================================================\n    // DATA PERSISTENCE & REAL-TIME FIRESTORE SYNC\n    // ============================================================"
marker_end = "    // ============================================================\n    // RENDERING ENGINES ACROSS ALL 4 CORE VIEWS"

idx_s = html.find(marker_start)
idx_e = html.find(marker_end)

if idx_s == -1 or idx_e == -1:
    print(f"Error finding markers: idx_s={idx_s}, idx_e={idx_e}")
else:
    new_sync_code = """    // ============================================================
    // DATA PERSISTENCE & REAL-TIME FIRESTORE SYNC (onSnapshot PIPELINE)
    // ============================================================
    function initDataSync(user) {
      currentUser = user;
      isDemoMode = !user || user.uid === 'demo-user';

      let stored = getLocalData();
      if (!stored) {
        stored = { goals: [], ledger: [] };
        saveLocalData(stored);
      }
      goals = stored.goals || [];
      ledger = stored.ledger || [];
      renderAll();

      if (isDemoMode || !db) return;

      try {
        if (unsubGoals) unsubGoals();
        if (unsubLedger) unsubLedger();

        // 1. Real-time Goals onSnapshot Listener
        const goalsCol = collection(db, 'users', user.uid, 'goals');
        unsubGoals = onSnapshot(goalsCol, (snapshot) => {
          goals = snapshot.docs.map(docSnap => ({ id: docSnap.id, ...docSnap.data() }));
          saveLocalData({ goals, ledger });
          renderAll();
        }, (err) => {
          console.error("Firestore Goals onSnapshot error:", err);
        });

        // 2. Real-time Ledger onSnapshot Listener (ordered by timestamp desc)
        const ledgerCol = collection(db, 'users', user.uid, 'ledger');
        const ledgerQuery = query(ledgerCol, orderBy('timestamp', 'desc'));

        const handleLedgerSnapshot = (snapshot) => {
          ledger = snapshot.docs.map(docSnap => {
            const data = docSnap.data();
            return {
              id: docSnap.id,
              ...data,
              amount: Number(data.amount) || 0,
              timestamp: data.timestamp?.toDate ? data.timestamp.toDate().toISOString() : (data.timestamp || new Date().toISOString())
            };
          });

          // Sort descending by date & timestamp
          ledger.sort((a, b) => new Date(b.date || b.timestamp) - new Date(a.date || a.timestamp));

          // Calculate current net capital: ADD adds, MINUS subtracts
          let runningTotal = 0;
          ledger.forEach(entry => {
            const amt = Number(entry.amount) || 0;
            if (entry.type === 'ADD') runningTotal += amt;
            else if (entry.type === 'MINUS') runningTotal -= amt;
          });
          if (runningTotal < 0) runningTotal = 0;

          // Immediately update #totalStashedDisplay with formatted sum
          const elTotal = document.getElementById('totalStashedDisplay') || document.getElementById('metric-total-capital');
          if (elTotal) elTotal.textContent = '₹' + runningTotal.toLocaleString('en-IN');

          saveLocalData({ goals, ledger });
          renderAll();
        };

        unsubLedger = onSnapshot(ledgerQuery, handleLedgerSnapshot, (err) => {
          console.error("Firestore Ledger onSnapshot error:", err);
          // Resilient fallback without order clause if index is building
          if (err.code === 'failed-precondition' || err.message?.includes('index')) {
            console.warn("Retrying ledger onSnapshot with base collection fallback...");
            unsubLedger = onSnapshot(ledgerCol, handleLedgerSnapshot, (fallbackErr) => {
              console.error("Firestore Ledger fallback onSnapshot error:", fallbackErr);
            });
          }
        });
      } catch (e) {
        console.error("Firestore sync initialization error:", e);
      }
    }

    async function persistGoal(goalData) {
      const localId = 'goal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4);
      const newGoal = {
        id: localId,
        ...goalData,
        createdAt: new Date().toISOString()
      };
      goals.push(newGoal);
      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const col = collection(db, 'users', currentUser.uid, 'goals');
        const docRef = await addDoc(col, { ...goalData, createdAt: serverTimestamp() });
        return { ...newGoal, id: docRef.id };
      }
      return newGoal;
    }

    async function persistLedgerEntry(entryData) {
      const isAdd = entryData.type === 'ADD';
      const amt = Number(entryData.amount) || 0;
      const delta = isAdd ? amt : -amt;

      // Optimistic local update
      const localId = 'tx-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4);
      const newEntry = {
        id: localId,
        ...entryData,
        amount: amt,
        timestamp: new Date().toISOString()
      };

      ledger.unshift(newEntry);

      const targetGoal = goals.find(g => g.id === entryData.goalId || g.name.toLowerCase() === (entryData.goalName || '').toLowerCase());
      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + delta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      // Real-time atomic Firestore write
      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const ledgerCol = collection(db, 'users', currentUser.uid, 'ledger');
        const docRef = await addDoc(ledgerCol, {
          type: entryData.type,
          amount: amt,
          note: entryData.note || '',
          date: entryData.date || new Date().toISOString().split('T')[0],
          goalId: entryData.goalId || '',
          goalName: entryData.goalName || '',
          timestamp: serverTimestamp()
        });

        // Atomically update /users/{uid} field totalSaved using increment(delta)
        const userRef = doc(db, 'users', currentUser.uid);
        await setDoc(userRef, { totalSaved: increment(delta) }, { merge: true });

        // Update goal balance in Firestore
        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal amount sync:", e));
        }

        return docRef.id;
      }
      return localId;
    }

    async function updateLedgerEntry(id, newAmount, newNote, newDate) {
      const existing = ledger.find(item => item.id === id);
      if (!existing) return;

      const oldAmount = Number(existing.amount) || 0;
      const amountDiff = newAmount - oldAmount;
      const isAdd = existing.type === 'ADD';
      const delta = isAdd ? amountDiff : -amountDiff;
      const targetGoal = goals.find(g => g.id === existing.goalId || g.name === existing.goalName);

      // Optimistic local update
      existing.amount = newAmount;
      existing.note = newNote;
      existing.date = newDate;

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + delta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        if (!id.startsWith('tx-')) {
          const ref = doc(db, 'users', currentUser.uid, 'ledger', id);
          await updateDoc(ref, { amount: newAmount, note: newNote, date: newDate });
        }

        if (delta !== 0) {
          const userRef = doc(db, 'users', currentUser.uid);
          await setDoc(userRef, { totalSaved: increment(delta) }, { merge: true });
        }

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }

    async function deleteLedgerEntry(id) {
      const existing = ledger.find(item => item.id === id);
      if (!existing) return;

      const isAdd = existing.type === 'ADD';
      const reversalDelta = isAdd ? -Number(existing.amount) : Number(existing.amount);
      const targetGoal = goals.find(g => g.id === existing.goalId || g.name === existing.goalName);

      ledger = ledger.filter(item => item.id !== id);

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + reversalDelta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        if (!id.startsWith('tx-')) {
          const ref = doc(db, 'users', currentUser.uid, 'ledger', id);
          await deleteDoc(ref);
        }

        const userRef = doc(db, 'users', currentUser.uid);
        await setDoc(userRef, { totalSaved: increment(reversalDelta) }, { merge: true });

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }

"""
    html = html[:idx_s] + new_sync_code + html[idx_e:]
    print("Replaced sync functions with async Firestore onSnapshot pipeline.")

# 3. Replace Modal Form Submissions with async handlers
# Target formCreateGoal
old_create_form = """    formCreateGoal?.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = goalInputName.value.trim();
      const amt = Number(goalInputAmount.value) || 0;
      const deadline = goalInputDeadline.value;

      let hasErr = false;
      if (!name) { document.getElementById('goal-err-name')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-name')?.classList.add('hidden');

      if (amt < 100) { document.getElementById('goal-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-amount')?.classList.add('hidden');

      if (!deadline) { document.getElementById('goal-err-deadline')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-deadline')?.classList.add('hidden');

      if (hasErr) return;

      lockBtn(btnCreateGoalSubmit, 'Locking...');

      persistGoal({
        name,
        targetAmount: amt,
        currentAmount: 0,
        deadline,
        cadence: selectedGoalCadence
      });

      setTimeout(() => {
        unlockBtn(btnCreateGoalSubmit);
        modalCreateGoal.classList.remove('open');
        goalInputName.value = '';
        goalInputAmount.value = '';
        goalInputDeadline.value = '';
        showToast(`🎯 Goal Vault "${name}" created!`, 'success');
        switchTab('goals');
      }, 120);
    });"""

new_create_form = """    formCreateGoal?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = goalInputName.value.trim();
      const amt = Number(goalInputAmount.value) || 0;
      const deadline = goalInputDeadline.value;

      let hasErr = false;
      if (!name) { document.getElementById('goal-err-name')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-name')?.classList.add('hidden');

      if (amt < 100) { document.getElementById('goal-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-amount')?.classList.add('hidden');

      if (!deadline) { document.getElementById('goal-err-deadline')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-deadline')?.classList.add('hidden');

      if (hasErr) return;

      lockBtn(btnCreateGoalSubmit, 'Locking...');

      try {
        await persistGoal({
          name,
          targetAmount: amt,
          currentAmount: 0,
          deadline,
          cadence: selectedGoalCadence
        });

        modalCreateGoal.classList.remove('open');
        goalInputName.value = '';
        goalInputAmount.value = '';
        goalInputDeadline.value = '';
        showToast(`🎯 Goal Vault "${name}" created!`, 'success');
        switchTab('goals');
      } catch (err) {
        console.error("Create goal error:", err);
        showToast('Error creating goal: ' + err.message, 'error');
      } finally {
        unlockBtn(btnCreateGoalSubmit);
      }
    });"""

if old_create_form in html:
    html = html.replace(old_create_form, new_create_form, 1)
    print("Updated formCreateGoal to async handler.")

# Target formAddSavings
old_add_form = """    formAddSavings?.addEventListener('submit', (e) => {
      e.preventDefault();
      const vaultName = addSelectedChip || addVaultInput.value.trim();
      const amt = Number(addAmountInput.value) || 0;
      const note = addNoteInput.value.trim() || 'Manual savings deposit';
      const date = addDateInput.value || `${nowY}-${nowM}-${nowD}`;

      let hasErr = false;
      if (!vaultName) { document.getElementById('add-err-vault')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('add-err-vault')?.classList.add('hidden');

      if (amt <= 0) { document.getElementById('add-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('add-err-amount')?.classList.add('hidden');

      if (hasErr) return;

      lockBtn(btnAddSavingsSubmit, 'Stashing...');

      const goalMatch = goals.find(g => g.name.toLowerCase() === vaultName.toLowerCase());
      const goalId = goalMatch ? goalMatch.id : 'custom-' + Date.now();

      persistLedgerEntry({
        goalId,
        goalName: vaultName,
        type: 'ADD',
        amount: amt,
        note,
        date
      });

      setTimeout(() => {
        modalAddSavings.classList.remove('open');
        clearAddChip();
        addAmountInput.value = '';
        addNoteInput.value = '';
        unlockBtn(btnAddSavingsSubmit);
        showToast(`+₹${amt.toLocaleString('en-IN')} added to "${vaultName}"! ⚡`, 'success');
      }, 120);
    });"""

new_add_form = """    formAddSavings?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const vaultName = addSelectedChip || addVaultInput.value.trim();
      const amt = Number(addAmountInput.value) || 0;
      const note = addNoteInput.value.trim() || 'Manual savings deposit';
      const date = addDateInput.value || `${nowY}-${nowM}-${nowD}`;

      let hasErr = false;
      if (!vaultName) { document.getElementById('add-err-vault')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('add-err-vault')?.classList.add('hidden');

      if (amt <= 0) { document.getElementById('add-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('add-err-amount')?.classList.add('hidden');

      if (hasErr) return;

      // Anti-Spam Single Click Lock
      lockBtn(btnAddSavingsSubmit, 'Stashing...');

      try {
        const goalMatch = goals.find(g => g.name.toLowerCase() === vaultName.toLowerCase());
        const goalId = goalMatch ? goalMatch.id : 'custom-' + Date.now();

        await persistLedgerEntry({
          goalId,
          goalName: vaultName,
          type: 'ADD',
          amount: amt,
          note,
          date
        });

        modalAddSavings.classList.remove('open');
        clearAddChip();
        addAmountInput.value = '';
        addNoteInput.value = '';
        showToast(`+₹${amt.toLocaleString('en-IN')} added to "${vaultName}"! ⚡`, 'success');
      } catch (err) {
        console.error("Add savings submission error:", err);
        showToast('Error saving deposit: ' + err.message, 'error');
      } finally {
        unlockBtn(btnAddSavingsSubmit);
      }
    });"""

if old_add_form in html:
    html = html.replace(old_add_form, new_add_form, 1)
    print("Updated formAddSavings to async handler.")

# Target formWithdrawal
old_with_form = """    formWithdrawal?.addEventListener('submit', (e) => {
      e.preventDefault();
      const goalId = withVaultSelect.value;
      const amt = Number(withAmountInput.value) || 0;
      const note = withNoteInput.value.trim();
      const date = withDateInput.value || `${nowY}-${nowM}-${nowD}`;

      let hasErr = false;
      if (!goalId) { document.getElementById('withdrawal-err-vault')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-vault')?.classList.add('hidden');

      if (amt <= 0) { document.getElementById('withdrawal-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-amount')?.classList.add('hidden');

      if (!note) { document.getElementById('withdrawal-err-note')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-note')?.classList.add('hidden');

      if (hasErr) return;

      lockBtn(btnWithdrawalSubmit, 'Recording...');

      const goalMatch = goals.find(g => g.id === goalId);
      const goalName = goalMatch ? goalMatch.name : 'Vault';

      persistLedgerEntry({
        goalId,
        goalName,
        type: 'MINUS',
        amount: amt,
        note,
        date
      });

      setTimeout(() => {
        unlockBtn(btnWithdrawalSubmit);
        modalWithdrawal.classList.remove('open');
        withAmountInput.value = '';
        withNoteInput.value = '';
        showToast(`-₹${amt.toLocaleString('en-IN')} withdrawal logged from "${goalName}".`, 'info');
      }, 120);
    });"""

new_with_form = """    formWithdrawal?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const goalId = withVaultSelect.value;
      const amt = Number(withAmountInput.value) || 0;
      const note = withNoteInput.value.trim();
      const date = withDateInput.value || `${nowY}-${nowM}-${nowD}`;

      let hasErr = false;
      if (!goalId) { document.getElementById('withdrawal-err-vault')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-vault')?.classList.add('hidden');

      if (amt <= 0) { document.getElementById('withdrawal-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-amount')?.classList.add('hidden');

      if (!note) { document.getElementById('withdrawal-err-note')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-note')?.classList.add('hidden');

      if (hasErr) return;

      // Anti-Spam Single Click Lock
      lockBtn(btnWithdrawalSubmit, 'Recording...');

      try {
        const goalMatch = goals.find(g => g.id === goalId);
        const goalName = goalMatch ? goalMatch.name : 'Vault';

        await persistLedgerEntry({
          goalId,
          goalName,
          type: 'MINUS',
          amount: amt,
          note,
          date
        });

        modalWithdrawal.classList.remove('open');
        withAmountInput.value = '';
        withNoteInput.value = '';
        showToast(`-₹${amt.toLocaleString('en-IN')} withdrawal logged from "${goalName}".`, 'info');
      } catch (err) {
        console.error("Withdrawal submission error:", err);
        showToast('Error recording withdrawal: ' + err.message, 'error');
      } finally {
        unlockBtn(btnWithdrawalSubmit);
      }
    });"""

if old_with_form in html:
    html = html.replace(old_with_form, new_with_form, 1)
    print("Updated formWithdrawal to async handler.")

# Target formEditLedger
old_edit_form = """    formEditLedger?.addEventListener('submit', (e) => {
      e.preventDefault();
      const id = editEntryId.value;
      const amt = Number(editEntryAmount.value) || 0;
      const note = editEntryNote.value.trim();
      const date = editEntryDate.value;

      if (!id || amt <= 0) return;

      lockBtn(btnEditLedgerSubmit, 'Saving...');
      updateLedgerEntry(id, amt, note, date);

      setTimeout(() => {
        unlockBtn(btnEditLedgerSubmit);
        modalEditLedger.classList.remove('open');
        showToast('Entry updated!', 'success');
      }, 120);
    });"""

new_edit_form = """    formEditLedger?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = editEntryId.value;
      const amt = Number(editEntryAmount.value) || 0;
      const note = editEntryNote.value.trim();
      const date = editEntryDate.value;

      if (!id || amt <= 0) return;

      lockBtn(btnEditLedgerSubmit, 'Saving...');

      try {
        await updateLedgerEntry(id, amt, note, date);
        modalEditLedger.classList.remove('open');
        showToast('Entry updated in real-time!', 'success');
      } catch (err) {
        console.error("Edit entry error:", err);
        showToast('Error updating entry: ' + err.message, 'error');
      } finally {
        unlockBtn(btnEditLedgerSubmit);
      }
    });"""

if old_edit_form in html:
    html = html.replace(old_edit_form, new_edit_form, 1)
    print("Updated formEditLedger to async handler.")

# Target btnDeleteLedgerConfirm
old_del_btn = """    btnDeleteLedgerConfirm?.addEventListener('click', () => {
      const id = deleteEntryId.value;
      if (!id) return;

      lockBtn(btnDeleteLedgerConfirm, 'Deleting...');
      deleteLedgerEntry(id);

      setTimeout(() => {
        unlockBtn(btnDeleteLedgerConfirm);
        modalDeleteLedger.classList.remove('open');
        showToast('Entry deleted & balance reversed.', 'info');
      }, 120);
    });"""

new_del_btn = """    btnDeleteLedgerConfirm?.addEventListener('click', async () => {
      const id = deleteEntryId.value;
      if (!id) return;

      lockBtn(btnDeleteLedgerConfirm, 'Deleting...');

      try {
        await deleteLedgerEntry(id);
        modalDeleteLedger.classList.remove('open');
        showToast('Entry deleted & balance reversed.', 'info');
      } catch (err) {
        console.error("Delete entry error:", err);
        showToast('Error deleting entry: ' + err.message, 'error');
      } finally {
        unlockBtn(btnDeleteLedgerConfirm);
      }
    });"""

if old_del_btn in html:
    html = html.replace(old_del_btn, new_del_btn, 1)
    print("Updated btnDeleteLedgerConfirm to async handler.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully! Length:", len(html))
