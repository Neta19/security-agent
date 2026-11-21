# דוח אבטחה: בדיקה חוזרת שנייה (אימות), neti-ad-agents-production
**תאריך:** 2026-11-21
**מה נבדק:** https://neti-ad-agents-production.up.railway.app
**כלים:** curl (16 בקשות GET, בערך אחת לשנייה, בלי התחברות, בלי טפסים ובלי סיסמה)

## סיכום
אין ממצאים לתיקון: 0 קריטי, 0 גבוה, 0 בינוני, 0 נמוך. התיקון מהבדיקה הקודמת אומת. ב-CSP יש עכשיו `base-uri 'self'`, `form-action 'self'` ו-`object-src 'none'`. נשארו שתי הערות ברמת "מידע" בלבד: `style-src 'unsafe-inline'`, שנשאר בכוונה, ו-`security.txt` ציבורי שחסר.

## ממצאים

### 1. `style-src 'unsafe-inline'` ב-CSP (נשאר בכוונה)
- **חומרה:** מידע
- **סעיף OWASP:** A02 Security Misconfiguration
- **איפה:** הכותרת `Content-Security-Policy` בכל התשובות
- **מה הבעיה:** ההגדרה מאפשרת עיצוב inline. הסיכון נמוך, כי `script-src` לא מוגדר בנפרד, ולכן חל עליו `default-src 'self'` וסקריפט inline חסום. בעלת האתר החליטה להשאיר את זה בינתיים כדי לא לשבור את העיצוב.
- **איך מתקנים (בעתיד, לא דחוף):** להעביר את העיצוב לקובצי CSS, או להשתמש ב-nonce או ב-hash, ואז להסיר את `'unsafe-inline'`.
- **איך מוודאים שתוקן:** `curl -sS --max-time 15 -D - -o /dev/null <url> | grep -i content-security-policy`. הערך `'unsafe-inline'` לא אמור להופיע.

### 2. אין `security.txt` ציבורי
- **חומרה:** מידע
- **סעיף OWASP:** A02 Security Misconfiguration
- **איפה:** `/.well-known/security.txt` מחזיר 401
- **מה הבעיה:** אין דרך ציבורית ומוסכמת לדווח על בעיות אבטחה. זה לא פגיעות.
- **איך מתקנים (אופציונלי):** לפתוח את הנתיב הזה לציבור עם קובץ שיש בו לפחות `Contact:` ו-`Expires:`.
- **איך מוודאים שתוקן:** `curl -sS --max-time 15 <url>/.well-known/security.txt` אמור להחזיר 200.

## נבדק ונמצא תקין
- **CSP (A02):** `default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'`. שלוש ההנחיות שנוספו קיימות ונכונות.
- **כותרות אבטחה (A02):** `Strict-Transport-Security: max-age=63072000; includeSubDomains`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Permissions-Policy` (camera, microphone, geolocation ו-payment חסומים), `Cache-Control: no-store`.
- **דליפת גרסה (A02):** `Server: railway-hikari` בלי מספר גרסה. אין `X-Powered-By`.
- **עוגיות (A07):** הדף הראשי לא שולח `Set-Cookie`.
- **HTTPS (A04):** `http://` מחזיר 301 ל-`https://`. אין בעיה בתעודה.
- **CORS (A02):** בקשה עם `Origin: https://example.com` לא החזירה `Access-Control-Allow-Origin` ולא `Access-Control-Allow-Credentials`.
- **דף שגיאה (A10):** נתיב שלא קיים מחזיר 401 קצר. אין stack trace, נתיבי קבצים, SQL או גרסאות.
- **קבצים שלא אמורים להיות ציבוריים (A01, A02):** כל הנתיבים הרגישים החזירו את אותה תשובה כמו ה-baseline (401, JSON של 38 בתים). אף קובץ לא חשוף. ה-401 האחיד מכוון ומסתיר אילו נתיבים קיימים. בקשות בלי סיסמה לא נספרות לנעילת הכניסה (אומת בקוד על ידי בעלת האתר).

## מה לא נבדק
- Nikto לא מותקן ולא הותקן. במקומו בוצעו הבדיקות העדינות.
- דפים ונתיבים שדורשים סיסמה לא נבדקו.
- לא נוסו טפסים, הגבלת ניסיונות כניסה בפועל או payloads.
- לא הייתה סקירת קוד (Bandit, תלויות, `npm audit` / `pip-audit`).
- נבדקו תשובות הדף הראשי בלבד, לא משאבי ה-JS וה-CSS שהוא טוען.

## הבקשות שנשלחו
16, כולן GET: דף הבית ב-https (200), דף הבית ב-http (301), דף הבית עם Origin זר (200), נתיב לא קיים (401), עשרת הנתיבים הרגישים (401), `/robots.txt` (401), `/.well-known/security.txt` (401).
