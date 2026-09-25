"""
SAVING GUIDE — CONTINUOUS AUTONOMOUS CONVERSATION ENGINE UPGRADE

Replaces:
1. BOT_KB (static rules) → Full BRAIN with numeric extraction, NLP classifiers,
   context memory, multi-turn follow-ups, dynamic math calculations
2. botRespond (one-shot, 5s delay) → Immediate continuous responder
3. Adds /system/admin_presence tracking
4. Instant SENT→DELIVERED→SEEN tick pipeline on every user message
5. Removes stale BOT_TIMEOUT logic
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

orig_len = len(html)
print(f"Original: {orig_len:,} bytes / {html.count(chr(10)):,} lines")

# ─────────────────────────────────────────────────────────────────────────────
# PATCH 1: Replace BOT_TIMEOUT constant + state vars with new vars
# ─────────────────────────────────────────────────────────────────────────────
OLD_STATE = """      const ADMIN_EMAIL  = 'karanak1513@gmail.com';
      const BOT_TIMEOUT  = 5000; // ms admin must reply before bot takes over

      // ── State ────────────────────────────────────────────────────
      let sgThreadId       = null;
      let sgWindowOpen     = false;
      let sgSendLock       = false;
      let sgBotLock        = false;
      let sgBotTimer       = null;
      let sgUnsubMsgs      = null;
      let sgUnsubThread    = null;
      let sgUnsubAdmin     = null;  // admin threads stream
      let sgUnsubAdminMsgs = null;  // admin selected thread messages
      let sgActiveThread   = null;  // admin: selected threadId
      let sgAdminSendLock  = false;
      let sgChatStatus     = 'BOT_AUTONOMOUS';"""

NEW_STATE = """      const ADMIN_EMAIL     = 'karanak1513@gmail.com';
      const PRESENCE_PATH   = 'system/admin_presence';
      const TYPING_MIN      = 600;   // ms min typing delay
      const TYPING_MAX      = 1200;  // ms max typing delay

      // ── State ────────────────────────────────────────────────────
      let sgThreadId        = null;
      let sgWindowOpen      = false;
      let sgSendLock        = false;
      let sgBotLock         = false;      // prevents concurrent bot replies
      let sgBotQueue        = [];         // pending user messages while bot is typing
      let sgUnsubMsgs       = null;
      let sgUnsubThread     = null;
      let sgUnsubAdmin      = null;       // admin threads stream
      let sgUnsubAdminMsgs  = null;       // admin selected thread messages
      let sgUnsubPresence   = null;       // admin presence listener
      let sgActiveThread    = null;       // admin: selected threadId
      let sgAdminSendLock   = false;
      let sgChatStatus      = 'BOT_AUTONOMOUS';
      let sgAdminOnline     = false;      // tracks live admin presence
      let sgConvContext     = {           // multi-turn memory
        lastIntent:   null,
        lastAmount:   null,
        lastDuration: null,
        lastGoal:     null,
        turnCount:    0
      };"""

if OLD_STATE in html:
    html = html.replace(OLD_STATE, NEW_STATE, 1)
    print("✅ State vars upgraded")
else:
    print("⚠️  State vars pattern not found")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 2: Replace entire BOT_KB + botMatch + botRespond with the new brain
# ─────────────────────────────────────────────────────────────────────────────
OLD_BOT_BRAIN_START = "      // ── BOT BRAIN ────────────────────────────────────────────\n      const BOT_KB = ["
OLD_BOT_BRAIN_END   = "        sgBotLock = false;\n      }"   # end of botRespond

start_idx = html.find(OLD_BOT_BRAIN_START)
# find the end of botRespond — search from start
end_search = html.find(OLD_BOT_BRAIN_END, start_idx)
if end_search == -1:
    print("⚠️  Could not find botRespond end, trying alternate...")
    OLD_BOT_BRAIN_END = "        sgBotLock = false;\n      }\n"
    end_search = html.find(OLD_BOT_BRAIN_END, start_idx)

if start_idx != -1 and end_search != -1:
    end_idx = end_search + len(OLD_BOT_BRAIN_END)
    old_brain = html[start_idx:end_idx]
    print(f"   Found bot brain block: L~{html[:start_idx].count(chr(10))+1} → {len(old_brain)} bytes")
else:
    print(f"⚠️  Brain block not found: start={start_idx}, end={end_search}")
    old_brain = None

NEW_BOT_BRAIN = r"""      // ================================================================
      // ░░  SAVING GUIDE — CONTINUOUS AUTONOMOUS BRAIN ENGINE  ░░
      // ================================================================

      // ── Admin Presence Tracking ──────────────────────────────────
      function heartbeatAdminPresence(isOnline) {
        if (!db || !currentUser || currentUser.email !== ADMIN_EMAIL) return;
        setDoc(doc(db, PRESENCE_PATH), {
          isOnline,
          lastSeen: serverTimestamp(),
          email: ADMIN_EMAIL
        }, { merge: true }).catch(() => {});
      }

      function watchAdminPresence() {
        if (!db) return;
        if (sgUnsubPresence) sgUnsubPresence();
        sgUnsubPresence = onSnapshot(doc(db, PRESENCE_PATH), (snap) => {
          sgAdminOnline = snap.exists() ? (snap.data().isOnline === true) : false;
        }, () => { sgAdminOnline = false; });
      }

      // ── Number / Duration Extractor ──────────────────────────────
      function extractNumbers(text) {
        // Extract amounts: "50000", "50,000", "50k", "1.5 lakh"
        const nums = [];
        const cleaned = text.toLowerCase();

        // Lakh pattern: "1.5 lakh", "2lakh"
        const lakhMatch = cleaned.match(/(\d+\.?\d*)\s*lakh/);
        if (lakhMatch) nums.push(Math.round(parseFloat(lakhMatch[1]) * 100000));

        // K pattern: "50k", "5k"
        const kMatch = cleaned.match(/(\d+\.?\d*)\s*k\b/);
        if (kMatch) nums.push(Math.round(parseFloat(kMatch[1]) * 1000));

        // Plain numbers with optional commas
        const plainMatches = [...cleaned.matchAll(/(\d{1,3}(?:,\d{3})*|\d+)/g)];
        plainMatches.forEach(m => {
          const n = parseInt(m[1].replace(/,/g, ''));
          if (n > 0 && !nums.includes(n)) nums.push(n);
        });

        return nums;
      }

      function extractDuration(text) {
        const lower = text.toLowerCase();
        // Days
        let m = lower.match(/(\d+)\s*(din|day|days)/);
        if (m) return { days: parseInt(m[1]), label: m[1] + ' din' };
        // Weeks
        m = lower.match(/(\d+)\s*(week|hafte)/);
        if (m) return { days: parseInt(m[1]) * 7, label: m[1] + ' hafte' };
        // Months
        m = lower.match(/(\d+)\s*(month|mahine|mahina|mah)/);
        if (m) return { days: parseInt(m[1]) * 30, label: m[1] + ' mahine' };
        // Years
        m = lower.match(/(\d+)\s*(year|sal|saal)/);
        if (m) return { days: parseInt(m[1]) * 365, label: m[1] + ' saal' };
        return null;
      }

      // ── NLP Intent Classifier ────────────────────────────────────
      const INTENT_MAP = [
        {
          name: 'SAVINGS_MATH',
          patterns: ['bachana', 'bacha', 'save karna', 'save krna', 'bachat', 'bachata', 'jama', 'target', 'goal amount',
                     'kitna bachana', 'how much', 'calculate', 'plan', 'lakh', 'thousand', '₹',
                     /\d+\s*(lakh|k\b|,000)/, /bachana.*din/, /din.*bachana/],
          detect: (lower, nums, dur) => (nums.length > 0 && (dur || lower.includes('din') || lower.includes('day') || lower.includes('mahine') || lower.includes('month')))
        },
        {
          name: 'HOW_TO_LOG',
          patterns: ['log', 'add kaise', 'add karun', 'deposit', 'how to save', 'save kaise', 'paisa add', 'record kaise',
                     'entry kaise', 'kaise add', 'kaise log'],
        },
        {
          name: 'GOAL_CREATE',
          patterns: ['goal banana', 'target banana', 'vault create', 'naya goal', 'new goal', 'goal kaise', 'target set',
                     'goal set', 'vault banana', 'create goal', 'goal banao'],
        },
        {
          name: 'WITHDRAWAL',
          patterns: ['withdraw', 'nikalna', 'nikalo', 'paisa nikalna', 'wapas', 'remove', 'minus'],
        },
        {
          name: 'SECURITY',
          patterns: ['real money', 'real paisa', 'bank connect', 'account', 'secure', 'safe', 'collect', 'linked', 'bank se',
                     'data safe', 'kya data', 'privacy'],
        },
        {
          name: 'LEDGER',
          patterns: ['ledger', 'history', 'record', 'purana', 'transactions', 'pichle', 'previous', 'all entries'],
        },
        {
          name: 'CALENDAR',
          patterns: ['calendar', 'streak', 'discipline', 'consistency', 'aaj ka', 'kitne din', 'how many days'],
        },
        {
          name: 'PROGRESS',
          patterns: ['progress', 'kitna bacha', 'how much saved', 'total', 'balance', 'kitna hai', 'current', 'abhi tak'],
        },
        {
          name: 'MOTIVATION',
          patterns: ['motivation', 'mushkil', 'difficult', 'hard', 'nahi ho raha', 'fail', 'chod dun', 'quit', 'de do',
                     'boring', 'kya fayda', 'why save', 'importance', 'zaruri'],
        },
        {
          name: 'GREETING',
          patterns: ['hello', 'hi', 'hey', 'hii', 'helo', 'namaste', 'namaskar', 'kya haal', 'sup', 'good morning',
                     'good evening', 'shubh', 'jai', 'sat sri akal', 'assalam'],
        },
        {
          name: 'THANKS',
          patterns: ['thank', 'thanks', 'shukriya', 'dhanyawad', 'bahut acha', 'bohot acha', 'amazing', 'perfect',
                     'helpful', 'great', 'superb', 'brilliant', 'wah'],
        },
        {
          name: 'HUMAN_AGENT',
          patterns: ['human', 'agent', 'karan', 'operator', 'live', 'manav', 'speak', 'baat', 'agent chahiye',
                     'talk to human', 'real person', 'insaan'],
        },
        {
          name: 'BUG_REPORT',
          patterns: ['bug', 'error', 'crash', 'not working', 'problem', 'issue', 'kaam nahi', 'broken', 'fix', 'glitch'],
        },
        {
          name: 'AFFIRM',
          patterns: ['haan', 'ha', 'yes', 'ok', 'okay', 'sure', 'bilkul', 'zaroor', 'theek hai', 'sahi', 'correct', 'right'],
        },
        {
          name: 'NEGATE',
          patterns: ['nahi', 'no', 'nope', 'mat', 'band karo', 'stop', 'skip', 'baad mein', 'later'],
        },
      ];

      function classifyIntent(text) {
        const lower = text.toLowerCase().trim();
        const nums  = extractNumbers(text);
        const dur   = extractDuration(text);

        // Special: savings math detection (amount + duration in same message)
        const mathIntent = INTENT_MAP.find(i => i.name === 'SAVINGS_MATH');
        if (mathIntent.detect && mathIntent.detect(lower, nums, dur)) {
          return { name: 'SAVINGS_MATH', nums, dur };
        }

        // Pattern matching
        for (const intent of INTENT_MAP) {
          if (!intent.patterns) continue;
          const matched = intent.patterns.some(p => {
            if (p instanceof RegExp) return p.test(lower);
            return lower.includes(p);
          });
          if (matched) return { name: intent.name, nums, dur };
        }

        // Only numbers — partial math intent
        if (nums.length > 0 && sgConvContext.lastIntent === 'SAVINGS_MATH') {
          return { name: 'SAVINGS_MATH_FOLLOWUP', nums, dur };
        }

        return { name: 'UNKNOWN', nums, dur };
      }

      // ── Reply Generator ──────────────────────────────────────────
      function generateReply(intent, userText) {
        const ctx = sgConvContext;
        ctx.turnCount++;
        const { name, nums, dur } = intent;

        // Helper: Indian number format
        const inr = n => '₹' + Number(n).toLocaleString('en-IN');

        // ── Savings Math Calculator ──────────────────────────────
        if (name === 'SAVINGS_MATH' || name === 'SAVINGS_MATH_FOLLOWUP') {
          const amount = nums[0] || ctx.lastAmount;
          const duration = dur || ctx.lastDuration || { days: 30, label: '1 mahine' };

          if (amount) {
            ctx.lastAmount   = amount;
            ctx.lastDuration = duration || ctx.lastDuration;
            ctx.lastIntent   = 'SAVINGS_MATH';

            const perDay   = Math.ceil(amount / duration.days);
            const perMonth = Math.ceil(perDay * 30);
            const perWeek  = Math.ceil(perDay * 7);

            return `📊 <strong>Aapka Savings Plan:</strong><br><br>` +
              `• <strong>Target:</strong> ${inr(amount)}<br>` +
              `• <strong>Samay:</strong> ${duration.label}<br>` +
              `• <strong>Rozana chahiye:</strong> ${inr(perDay)}/din<br>` +
              `• <strong>Hafte mein:</strong> ${inr(perWeek)}/week<br>` +
              `• <strong>Mahine mein:</strong> ${inr(perMonth)}/month<br><br>` +
              `Kya aap iske liye <strong>Goals tab mein target set karna chahenge?</strong> Main aapko step-by-step guide karunga. 🎯`;
          }

          // Amount missing — ask for it
          ctx.lastIntent = 'SAVINGS_MATH';
          if (dur) {
            ctx.lastDuration = dur;
            return `💰 ${dur.label} mein aap kitna save karna chahte hain? <strong>Amount batayein</strong> (jaise "50000" ya "1 lakh") aur main aapka daily quota calculate kar dunga. 🧮`;
          }
          return `💰 Savings plan banate hain! <strong>Kitna amount bachana hai</strong> aur <strong>kitne din/mahine mein</strong>? Jaise: "50,000 rupees in 3 months"`;
        }

        // ── Follow-up: after savings math was shown ─────────────
        if (ctx.lastIntent === 'SAVINGS_MATH' && name === 'AFFIRM') {
          ctx.lastIntent = 'GOAL_CREATE';
          return `🎯 <strong>Goal banana bilkul easy hai:</strong><br><br>1. <strong>Goals tab</strong> open karo (bottom navigation)<br>2. <strong>"+ Create Target Vault"</strong> tap karo<br>3. Amount: <strong>${ctx.lastAmount ? inr(ctx.lastAmount) : 'apna amount'}</strong> enter karo<br>4. Deadline set karo<br><br>App apne aap daily/monthly quota calculate kar dega. ✅<br><br><em>Kya aap abhi goals tab open karna chahte hain?</em>`;
        }

        if (ctx.lastIntent === 'SAVINGS_MATH' && name === 'NEGATE') {
          return `No problem! 😊 Jab bhi savings plan banana ho, main yahan hoon.<br><br>Aur kuch puchna hai? Jaise — ledger dekhna, withdrawal karna, ya koi aur sawaal?`;
        }

        // ── Greeting ─────────────────────────────────────────────
        if (name === 'GREETING') {
          ctx.lastIntent = 'GREETING';
          const greetings = [
            `👋 <strong>Namaste!</strong> Main Saving Guide hoon — aapka personal savings discipline assistant. 🛡<br><br>Aaj main aapki kya madad kar sakta hoon?<br>• 💰 Savings plan calculate karna<br>• 🎯 New goal set karna<br>• 📒 Records check karna<br>• 🔒 Security questions<br><br><em>Bas type karein — main yahan hoon!</em>`,
            `🙏 <strong>Namaste ji!</strong> Saving Guide hazir hai. Aapka savings safar kaisa chal raha hai?<br><br>Kya aaj kuch save kiya? Ya koi naya goal set karna hai?`,
            `👋 Hey! Saving Guide here. Paise bachane ka <em>sahi time</em> abhi hai — main aapki puri help karunga.<br><br>Kya aap savings calculate karna chahte hain ya pehle current balance check karein?`
          ];
          return greetings[Math.floor(Math.random() * greetings.length)];
        }

        // ── Thanks ───────────────────────────────────────────────
        if (name === 'THANKS') {
          ctx.lastIntent = 'THANKS';
          return `😊 Bahut khushi hui! <strong>Aapka savings safar bahut inspiring hai.</strong><br><br>Kuch aur help chahiye? Main hamesha yahan hoon. Aur ek baat — <em>choti-choti savings mili kar badi ban jaati hain!</em> 💪<br><br>Aaj kitna save karne ka plan hai?`;
        }

        // ── How to Log ───────────────────────────────────────────
        if (name === 'HOW_TO_LOG') {
          ctx.lastIntent = 'HOW_TO_LOG';
          return `💰 <strong>Savings log karna super easy hai:</strong><br><br>1. Dashboard pe <strong>"+ Add Saved"</strong> button tap karo<br>2. Amount enter karo (cash ya UPI — dono same hai)<br>3. Goal select karo (optional)<br>4. <strong>Confirm</strong> — vault instantly update! ⚡<br><br><em>Koi bank link nahi hota. Sirf aap apna discipline track karte ho.</em><br><br>Kya aap abhi kuch save karna chahte hain? Kitna amount?`;
        }

        // ── Goal Create ──────────────────────────────────────────
        if (name === 'GOAL_CREATE') {
          ctx.lastIntent = 'GOAL_CREATE';
          return `🎯 <strong>Goal create karna:</strong><br><br>1. Bottom navigation mein <strong>Goals</strong> tab tapein<br>2. <strong>"+ Create Target Vault"</strong> par click karein<br>3. Goal naam dein (jaise "Emergency Fund", "iPhone", "Trip")<br>4. Target amount aur deadline set karein<br>5. Cadence choose karein: <strong>Daily / Monthly / Yearly</strong><br><br>App automatically calculate karega: <em>Agar aapko 30 din mein ₹10,000 chahiye toh roz ₹334 bachana hoga</em>. 📊<br><br>Kaunsa goal banana hai aapka? Amount bataiye — main plan calculate kar deta hoon!`;
        }

        // ── Withdrawal ───────────────────────────────────────────
        if (name === 'WITHDRAWAL') {
          ctx.lastIntent = 'WITHDRAWAL';
          return `🏦 <strong>Withdrawal record karna:</strong><br><br>1. Home screen pe <strong>"− Record Withdrawal"</strong> tapein<br>2. Vault choose karein<br>3. Amount enter karein<br>4. Reason likhein (optional)<br><br>Balance instantly update ho jayega aur ledger mein entry aa jayegi. ✅<br><br>Kitna withdraw karna chahte hain? Koi specific reason hai — emergency, planned expense?`;
        }

        // ── Security ─────────────────────────────────────────────
        if (name === 'SECURITY') {
          ctx.lastIntent = 'SECURITY';
          return `🔒 <strong>100% Safe — Yahan koi real paisa nahi rakhha jaata.</strong><br><br>SaveMoneyManually ek <em>discipline tracker</em> hai:<br>• ❌ Koi bank account link nahi hota<br>• ❌ Koi payment gateway nahi<br>• ❌ Koi real fund collection nahi<br>• ✅ Aap khud apne cash/UPI savings alag rakhte ho<br>• ✅ Yahan sirf aap <em>track</em> karte ho<br>• ✅ Firebase 256-bit encryption se data secure hai<br><br>Aapka data sirf aapke Google account se linked hai. 🛡<br><br>Aur koi security sawaal hai?`;
        }

        // ── Ledger ───────────────────────────────────────────────
        if (name === 'LEDGER') {
          ctx.lastIntent = 'LEDGER';
          return `📒 <strong>Aapka Ledger / History:</strong><br><br>Bottom navigation mein <strong>Ledger</strong> tab tapein. Wahan aap:<br>• Saare deposits aur withdrawals chronologically dekhenge<br>• Koi bhi entry <strong>edit</strong> kar sakte hain<br>• Koi bhi entry <strong>delete</strong> kar sakte hain<br><br>Saari changes real-time mein sync hoti hain instantly. ⚡<br><br>Kya aap koi specific entry dhundh rahe hain ya overall balance check karna hai?`;
        }

        // ── Calendar / Streak ─────────────────────────────────────
        if (name === 'CALENDAR') {
          ctx.lastIntent = 'CALENDAR';
          return `📅 <strong>Calendar Streak:</strong><br><br>Bottom nav mein <strong>Calendar</strong> tap karein.<br><br>Jis din aapne saving log ki — woh <strong>Electric Blue</strong> se highlight hogi. Continuous streak banao — <em>consistency hi real wealth hai</em>. 🔥<br><br>Research kehti hai: <strong>66 din ki daily savings habit</strong> permanent ban jaati hai.<br><br>Aaj ki saving log ki? Aur kitne din ka streak hai abhi?`;
        }

        // ── Progress / Balance ────────────────────────────────────
        if (name === 'PROGRESS') {
          ctx.lastIntent = 'PROGRESS';
          return `📊 <strong>Aapka progress dashboard pe live dikh raha hai!</strong><br><br>Home screen open karein — wahan:<br>• <strong>Total Capital</strong> — ab tak jitna bacha hai<br>• <strong>This Month</strong> — is mahine ki savings<br>• <strong>Active Goals</strong> — har vault ka progress<br><br>Sab kuch real-time Firestore se sync hota hai. ⚡<br><br>Kya aap kisi specific goal ka progress dekhna chahte hain? Ya naya saving add karna hai?`;
        }

        // ── Motivation ────────────────────────────────────────────
        if (name === 'MOTIVATION') {
          ctx.lastIntent = 'MOTIVATION';
          const motivations = [
            `💪 <strong>Mushkil lagta hai — bilkul normal hai!</strong><br><br>Savings discipline ek skill hai, ek talent nahi. Pehle 2-3 hafte hardest hote hain.<br><br>Ek simple trick: <em>"Pay yourself first"</em> — jab bhi income aaye, pehle 10% side rakh do, baad mein baki kharch karo.<br><br>Aap daily kitna afford kar sakte hain realistically? Main ek achievable plan banata hoon aapke liye. 🎯`,
            `🌟 <strong>Har badi savings choti starting se hoti hai.</strong><br><br>Sirf ₹100/din bachao — 1 saal mein ₹36,500 ho jaata hai. Bina kuch extra kiye.<br><br>Aap abhi kahan hain apni journey mein? Naya shuru karna hai ya pehle se chal raha hai?`,
            `🔥 <strong>Chod dene ka mann? Main samajhta hoon.</strong><br><br>Lekin ek baar apna original goal yaad karo — <em>kyun shuru kiya tha?</em><br><br>Woh reason aaj bhi valid hai. App band karo, kal wapas aao — main hoon. Aur kal fir ek ₹1 bachao — bas itna kaafi hai. 💙`
          ];
          return motivations[Math.floor(Math.random() * motivations.length)];
        }

        // ── Human Agent ──────────────────────────────────────────
        if (name === 'HUMAN_AGENT') {
          ctx.lastIntent = 'HUMAN_AGENT';
          return `🔗 <strong>Samajh gaya!</strong> Maine Karan ko notification bhej di hai.<br><br>Wo jald hi join karenge. Tab tak — kya main aapki kuch aur help kar sakta hoon? Aapka kya sawaal tha originally? 🙏`;
        }

        // ── Bug Report ───────────────────────────────────────────
        if (name === 'BUG_REPORT') {
          ctx.lastIntent = 'BUG_REPORT';
          return `🛠 <strong>Issue report kiya — shukriya!</strong><br><br>Pehle yeh try karein:<br>1. Page <strong>refresh</strong> karein (Ctrl+R / Pull to refresh)<br>2. Browser cache clear karein<br>3. Doosre browser mein try karein<br><br>Agar phir bhi nahi chala — <strong>kya exactly ho raha hai?</strong> Screenshot ya error message copy karein — main Karan tak pahuncha dunga. 🔧`;
        }

        // ── Affirm (generic) ─────────────────────────────────────
        if (name === 'AFFIRM') {
          if (ctx.lastIntent === 'HOW_TO_LOG') {
            return `💰 <strong>Badiya!</strong> Dashboard pe jaiye aur <strong>"+ Add Saved"</strong> tap karein. Kitna amount add karna hai?`;
          }
          if (ctx.lastIntent === 'GOAL_CREATE') {
            return `🎯 <strong>Perfect!</strong> Goals tab mein <strong>"+ Create Target Vault"</strong> tap karein. Kaunsa goal banana hai — naam aur amount bataiye!`;
          }
          return `👍 <strong>Bilkul!</strong> Toh hum aage badhte hain — ${ctx.lastIntent === 'GREETING' ? 'aapko kya help chahiye aaj?' : 'Aur kuch puchna hai?'}`;
        }

        // ── Negate (generic) ─────────────────────────────────────
        if (name === 'NEGATE') {
          return `No problem! 😊 Kab bhi zarurat ho, main yahan hoon.<br><br>Aur koi sawaal hai — savings, goals, ledger, ya kuch bhi? Bas type karein. 🛡`;
        }

        // ── UNKNOWN / Open-Ended — Natural Fallback ───────────────
        ctx.lastIntent = 'UNKNOWN';
        const fallbacks = [
          `🤔 <strong>Interesting sawaal!</strong> Mujhe thoda aur context chahiye.<br><br>Kya aap in mein se kuch puchna chahte hain?`,
          `💭 Main samajhna chahta hoon — <strong>thoda aur detail mein batayein?</strong><br><br>Ya seedha bata dein: savings add karni hai, goal banana hai, ya koi aur kaam?`,
          `🛡 Aapka sawaal interesting hai! Yeh topics main <strong>bahut achhe se guide kar sakta hoon:</strong>`,
          `❓ <strong>Hm, ye mujhse thoda bahar hai</strong> — lekin chinta mat karein! Yeh cheezein main zaroor help kar sakta hoon:`,
        ];
        return fallbacks[Math.floor(Math.random() * fallbacks.length)];
      }

      // ── Typing delay ─────────────────────────────────────────────
      function typingDelay(text) {
        // Longer texts = slightly longer delay (realism), capped at TYPING_MAX
        const base = TYPING_MIN;
        const extra = Math.min(text.length * 2, TYPING_MAX - TYPING_MIN);
        return base + extra * Math.random();
      }

      // ── Core bot respond function ─────────────────────────────────
      async function botRespond(userText) {
        // Don't respond if admin is live
        if (sgChatStatus === 'ADMIN_LIVE') {
          sgBotLock = false;
          return;
        }

        // If already typing, queue the message
        if (sgBotLock) {
          sgBotQueue.push(userText);
          return;
        }
        sgBotLock = true;

        // Mark user's last message as SEEN immediately (tick turns blue)
        if (db && sgThreadId) {
          try {
            const msgsSnap = await getDocs(
              query(collection(db, 'support_threads', sgThreadId, 'messages'),
                orderBy('timestamp', 'desc'),
                limit(1))
            );
            msgsSnap.forEach(d => {
              if (d.data().sender === 'USER') {
                updateDoc(d.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          } catch (e) {}
        }

        // Show typing indicator
        showTyping('Saving Guide is typing…');

        const intent = classifyIntent(userText);
        const replyText = generateReply(intent, userText);
        const delay = typingDelay(replyText.replace(/<[^>]*>/g, ''));

        await new Promise(res => setTimeout(res, delay));
        hideTyping();

        // Write bot reply to Firestore (onSnapshot renders it)
        if (db && sgThreadId) {
          try {
            await addDoc(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'SAVING_GUIDE', text: replyText, status: 'DELIVERED', timestamp: serverTimestamp() }
            );
            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: replyText.replace(/<[^>]*>/g, '').substring(0, 80),
              lastMessageTime: serverTimestamp()
            });
          } catch (e) { console.warn('Bot write error:', e); }
        }

        // Handle special actions
        if (intent.name === 'HUMAN_AGENT') {
          if (db && sgThreadId) {
            updateDoc(doc(db, 'support_threads', sgThreadId), { chatStatus: 'ADMIN_LIVE' }).catch(() => {});
          }
          sgChatStatus = 'ADMIN_LIVE';
          setHeaderState('requesting');
        } else if (intent.name === 'UNKNOWN') {
          // Show pills after a short gap on unknown intents
          setTimeout(() => {
            if (sgChatStatus === 'BOT_AUTONOMOUS') renderPills(DEFAULT_PILLS);
          }, 400);
        }

        sgBotLock = false;

        // Process queued messages (multi-turn)
        if (sgBotQueue.length > 0 && sgChatStatus === 'BOT_AUTONOMOUS') {
          const next = sgBotQueue.shift();
          botRespond(next);
        }
      }
"""

if old_brain and start_idx != -1:
    html = html[:start_idx] + NEW_BOT_BRAIN + html[end_idx:]
    print(f"✅ Bot brain replaced: {len(old_brain)} bytes → {len(NEW_BOT_BRAIN)} bytes")
else:
    print("⚠️  Bot brain replacement skipped — block not found")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 3: Fix handleUserSend — add immediate SENT→DELIVERED tick + no BOT_TIMEOUT
# ─────────────────────────────────────────────────────────────────────────────
OLD_SEND = """      // ── Handle user send ─────────────────────────────────────────
      async function handleUserSend(overrideText) {
        if (sgSendLock) return;
        const text = (overrideText || elInput?.value || '').trim();
        if (!text || !currentUser) return;
        sgSendLock = true;
        if (elInput && !overrideText) elInput.value = '';

        // Cancel pending bot timer if admin was going to be waited for
        if (sgBotTimer) { clearTimeout(sgBotTimer); sgBotTimer = null; }

        // Optimistic UI
        const optimisticWrap = renderMsg(null, 'USER', text, 'SENT', new Date());

        // Write to Firestore
        let msgDocId = null;
        if (db && sgThreadId) {
          try {
            const ref = await addDoc(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'USER', text, status: 'SENT', timestamp: serverTimestamp() }
            );
            msgDocId = ref.id;
            // Update to DELIVERED
            await updateDoc(ref, { status: 'DELIVERED' });
            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: text.substring(0,80),
              lastMessageTime: serverTimestamp(),
              adminUnread: increment(1)
            });
            // Update optimistic tick to delivered
            updateMessageTick(optimisticWrap, 'DELIVERED');
          } catch (e) { console.warn('User msg write error:', e); }
        }

        sgSendLock = false;

        // If bot autonomous → bot will reply (with 5s admin window)
        if (sgChatStatus === 'BOT_AUTONOMOUS') {
          botRespond(text);
        }
      }"""

NEW_SEND = """      // ── Handle user send ─────────────────────────────────────────
      async function handleUserSend(overrideText) {
        if (sgSendLock) return;
        const text = (overrideText || elInput?.value || '').trim();
        if (!text || !currentUser) return;
        sgSendLock = true;
        if (elInput && !overrideText) elInput.value = '';

        // Render optimistic bubble immediately (SENT = ✓ gray)
        const optimisticWrap = renderMsg(null, 'USER', text, 'SENT', new Date());

        // Enable send button immediately after optimistic render
        sgSendLock = false;

        // Write to Firestore: SENT → DELIVERED in rapid succession
        if (db && sgThreadId) {
          try {
            const ref = await addDoc(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'USER', text, status: 'SENT', timestamp: serverTimestamp() }
            );

            // Immediately upgrade to DELIVERED (✓✓ gray)
            await updateDoc(ref, { status: 'DELIVERED' });
            updateMessageTick(optimisticWrap, 'DELIVERED');

            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: text.substring(0, 80),
              lastMessageTime: serverTimestamp(),
              adminUnread: increment(1)
            });
          } catch (e) {
            console.warn('User msg write error:', e);
          }
        }

        // Bot responds immediately — no timer delay needed
        // Admin presence check: if admin online and ADMIN_LIVE, skip bot
        if (sgChatStatus === 'BOT_AUTONOMOUS' && !sgAdminOnline) {
          botRespond(text);
        } else if (sgChatStatus === 'BOT_AUTONOMOUS' && sgAdminOnline) {
          // Admin is online but hasn't taken over — bot still responds after short pause
          setTimeout(() => {
            if (sgChatStatus === 'BOT_AUTONOMOUS') botRespond(text);
          }, 2000);
        }
        // If ADMIN_LIVE: admin replies via desk — bot stays silent
      }"""

if OLD_SEND in html:
    html = html.replace(OLD_SEND, NEW_SEND, 1)
    print("✅ handleUserSend upgraded with instant tick pipeline")
else:
    print("⚠️  handleUserSend pattern not found — trying partial match")
    # Try patching just the bot timer cancel + 5s timeout part
    if "if (sgBotTimer) { clearTimeout(sgBotTimer); sgBotTimer = null; }" in html:
        html = html.replace(
            "        // Cancel pending bot timer if admin was going to be waited for\n        if (sgBotTimer) { clearTimeout(sgBotTimer); sgBotTimer = null; }",
            "        // No admin timer needed — bot responds immediately",
            1
        )
        print("✅ Removed BOT_TIMEOUT timer cancel")
    if "// If bot autonomous → bot will reply (with 5s admin window)" in html:
        html = html.replace(
            "        // If bot autonomous → bot will reply (with 5s admin window)\n        if (sgChatStatus === 'BOT_AUTONOMOUS') {\n          botRespond(text);\n        }",
            "        // Bot responds immediately (no timer delay)\n        if (sgChatStatus === 'BOT_AUTONOMOUS' && !sgAdminOnline) {\n          botRespond(text);\n        } else if (sgChatStatus === 'BOT_AUTONOMOUS' && sgAdminOnline) {\n          setTimeout(() => { if (sgChatStatus === 'BOT_AUTONOMOUS') botRespond(text); }, 2000);\n        }",
            1
        )
        print("✅ Patched bot dispatch in handleUserSend")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 4: Add admin presence heartbeat when admin console opens/closes
# ─────────────────────────────────────────────────────────────────────────────
OLD_ADMIN_OPEN = """      elAdminOverlay?.addEventListener('click', (e) => {
        if (e.target === elAdminOverlay) elAdminOverlay.classList.remove('open');
      });
      elAdminClose?.addEventListener('click', () => elAdminOverlay?.classList.remove('open'));"""

NEW_ADMIN_OPEN = """      elAdminOverlay?.addEventListener('click', (e) => {
        if (e.target === elAdminOverlay) {
          elAdminOverlay.classList.remove('open');
          heartbeatAdminPresence(false);
        }
      });
      elAdminClose?.addEventListener('click', () => {
        elAdminOverlay?.classList.remove('open');
        heartbeatAdminPresence(false);
      });"""

if OLD_ADMIN_OPEN in html:
    html = html.replace(OLD_ADMIN_OPEN, NEW_ADMIN_OPEN, 1)
    print("✅ Admin presence heartbeat on close injected")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 5: Inject presence tracking into openAdminConsole function
# ─────────────────────────────────────────────────────────────────────────────
OLD_ADMIN_BTN = """          ab.addEventListener('click', () => elAdminOverlay?.classList.add('open'));"""
NEW_ADMIN_BTN = """          ab.addEventListener('click', () => {
            elAdminOverlay?.classList.add('open');
            heartbeatAdminPresence(true);
            // Keep presence alive every 30s
            if (window._adminHeartbeatInterval) clearInterval(window._adminHeartbeatInterval);
            window._adminHeartbeatInterval = setInterval(() => {
              if (elAdminOverlay?.classList.contains('open')) heartbeatAdminPresence(true);
              else { clearInterval(window._adminHeartbeatInterval); heartbeatAdminPresence(false); }
            }, 30000);
          });"""

if OLD_ADMIN_BTN in html:
    html = html.replace(OLD_ADMIN_BTN, NEW_ADMIN_BTN, 1)
    print("✅ Admin heartbeat interval injected")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 6: Call watchAdminPresence inside __sgInit
# ─────────────────────────────────────────────────────────────────────────────
OLD_SGINIT = """        ensureThread(user);
        if (isAdmin(user)) initAdminDesk(user);"""

NEW_SGINIT = """        watchAdminPresence();
        ensureThread(user);
        if (isAdmin(user)) initAdminDesk(user);"""

if OLD_SGINIT in html:
    html = html.replace(OLD_SGINIT, NEW_SGINIT, 1)
    print("✅ watchAdminPresence() called on user login")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH 7: Add getDocs + limit imports (needed for SEEN tick in botRespond)
# ─────────────────────────────────────────────────────────────────────────────
# Check if getDocs is imported
if 'getDocs,' not in html and 'getDocs }' not in html and "'getDocs'" not in html:
    # Find firebase import line
    old_import = "import { collection, doc, setDoc, addDoc, updateDoc, deleteDoc, getDoc, onSnapshot, query, orderBy, serverTimestamp, increment } from"
    new_import = "import { collection, doc, setDoc, addDoc, updateDoc, deleteDoc, getDoc, getDocs, onSnapshot, query, orderBy, limit, serverTimestamp, increment } from"
    if old_import in html:
        html = html.replace(old_import, new_import, 1)
        print("✅ Added getDocs + limit to Firestore imports")
    else:
        # Try to find any firebase/firestore import
        import re
        pattern = r"import \{([^}]+)\} from ['\"]https://www\.gstatic\.com/firebasejs/[^'\"]+/firebase-firestore[^'\"]*['\"]"
        match = re.search(pattern, html)
        if match:
            old_imp = match.group(0)
            if 'getDocs' not in old_imp:
                new_imp = old_imp.replace('onSnapshot,', 'getDocs, onSnapshot,').replace('orderBy,', 'orderBy, limit,')
                html = html.replace(old_imp, new_imp, 1)
                print("✅ Added getDocs + limit via regex import patch")
        else:
            print("⚠️  Could not find Firestore import line for getDocs")
else:
    print("ℹ️  getDocs already imported")

# Also add limit if not present
if ', limit,' not in html and ', limit }' not in html:
    html = html.replace('import { collection, doc, setDoc, addDoc, updateDoc, deleteDoc, getDoc, getDocs, onSnapshot, query, orderBy,',
                       'import { collection, doc, setDoc, addDoc, updateDoc, deleteDoc, getDoc, getDocs, onSnapshot, query, orderBy, limit,', 1)


# ─────────────────────────────────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Done! Final: {len(html):,} bytes / {html.count(chr(10)):,} lines")
print(f"   Delta: {len(html) - orig_len:+,} bytes")
