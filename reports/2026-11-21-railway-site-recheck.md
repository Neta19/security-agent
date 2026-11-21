# דוח אבטחה: בדיקה חוזרת (אימות) של neti-ad-agents-production.up.railway.app
**תאריך:** 2026-11-21
**מה נבדק:** https://neti-ad-agents-production.up.railway.app (אתר חי, סעיפים 4.1 עד 4.4 בלבד)
**כלים:** curl (16 בקשות GET, בערך אחת לשנייה, בלי התחברות, בלי טפסים, בלי סיסמה)

## סיכום
בבדיקה החוזרת לא נמצאו ממצאים ברמת קריטי, גבוה או בינוני. הכותרת `Permissions-Policy` שהייתה חסרה בבדיקה הראשונה נמצאת עכשיו בכל התשובות, אז הממצא הזה תוקן. נשאר ממצא אחד ברמה נמוכה (אפשר להקשיח עוד את ה-CSP) וממצא אחד ברמת מידע (`security.txt` לא זמין לציבור). אין שום דבר דחוף לתקן.

## ממצאים

### 1. אפשר להקשיח עוד את ה-Content-Security-Policy
- **חומרה:** נמוך
- **סעיף OWASP:** A02 Security Misconfiguration
- **איפה:** הכותרת `content-security-policy` בכל התשובות
- **מה הבעיה:** המדיניות הנוכחית היא `default-src 'self'; img-src 'self' data: blob:; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'`. היא טובה, אבל יש בה שלושה פערים קטנים:
  - `style-src 'unsafe-inline'` מתיר עיצוב שמוטמע בתוך הדף.
  - חסרים `base-uri` ו-`form-action`. שתי ההנחיות האלה לא נופלות חזרה ל-`default-src`, ולכן כרגע אין עליהן שום הגבלה.
  - חסר `object-src 'none'` מפורש.
- **איך מתקנים:** להוסיף `base-uri 'self'; form-action 'self'; object-src 'none'`. אם אפשר, להעביר את העיצוב המוטמע לקבצי CSS חיצוניים (או להשתמש ב-nonce/hash), ואז להסיר את `'unsafe-inline'`.
- **איך מוודאים שתוקן:** `curl -sS --max-time 15 -D - -o /dev/null <url> | grep -i content-security-policy` ולבדוק שההנחיות החדשות מופיעות.

### 2. הקובץ security.txt לא זמין לציבור
- **חומרה:** מידע
- **סעיף OWASP:** A02 Security Misconfiguration (מידע בלבד)
- **איפה:** `/.well-known/security.txt`
- **מה הבעיה:** הנתיב מחזיר 401 כמו כל נתיב לא ציבורי, ולכן לחוקר אבטחה אין דרך מסודרת לדווח על בעיה. גם `/robots.txt` מחזיר 401. זה לא מזיק, ומתאים להחלטה לנעול את כל הנתיבים.
- **איך מתקנים (לא חובה):** לפתוח לציבור רק את `/.well-known/security.txt` ולשים בו שורת `Contact:` ושורת `Expires:`.
- **איך מוודאים שתוקן:** `curl -sS --max-time 15 <url>/.well-known/security.txt` אמור להחזיר 200 עם שורת `Contact:`.

## מה נבדק ונמצא תקין
- **Permissions-Policy (התיקון מהבדיקה הראשונה):** קיים עכשיו: `camera=(), microphone=(), geolocation=(), payment=()`. מופיע בדף הראשי וגם בתשובות 401.
- **שאר כותרות האבטחה:** `Strict-Transport-Security: max-age=63072000; includeSubDomains`, `X-Frame-Options: DENY`, `frame-ancestors 'none'` ב-CSP, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store`.
- **חשיפת גרסאות:** `Server: railway-hikari` בלי מספר גרסה. אין `X-Powered-By`.
- **עוגיות:** הדף הראשי לא שולח `Set-Cookie`.
- **HTTPS:** `http://` מחזיר 301 ל-`https://`. אין בעיה בתעודה.
- **CORS:** בקשה עם `Origin: https://example.com` לא החזירה `Access-Control-Allow-Origin`. אין גישה פתוחה מאתרים אחרים.
- **דף שגיאה:** נתיב שלא קיים מחזיר 401 קצר, בלי stack trace, נתיבי קבצים או גרסאות.
- **קבצים שלא אמורים להיות ציבוריים:** כל עשרת הנתיבים החזירו תשובה זהה לתשובת הבסיס. אף קובץ לא נחשף.
- **401 זהה לכל נתיב לא ציבורי:** החלטה מכוונת של בעלת האתר, כדי להסתיר אילו נתיבים קיימים. נבדק בקוד שבקשות בלי סיסמה לא נספרות לנעילת ההתחברות. לא מדווח כממצא.

## מה לא נבדק
- Nikto לא מותקן ולא הותקן. במקומו בוצעו הבדיקות העדינות.
- דפים ו-API שדורשים סיסמה לא נבדקו: בקרת גישה אחרי התחברות, עוגיות session והגבלת ניסיונות כניסה.
- לא נבדקה בקשת preflight (`OPTIONS`) ל-CORS.
- לא בוצעה סקירת קוד (לא Bandit, לא `npm audit` / `pip-audit`).

## הבקשות שנשלחו
16, כולן GET: דף הבית ב-https (200), דף הבית ב-http (301), דף הבית עם Origin זר (200), נתיב לא קיים (401), עשרת הנתיבים הרגישים (401, זהה לבסיס), `/robots.txt` (401), `/.well-known/security.txt` (401).
