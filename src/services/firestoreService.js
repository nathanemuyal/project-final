import { db } from '../firebase/firebase';
import { doc, getDoc, setDoc, collection } from 'firebase/firestore';
import { auth } from 'firebase/auth';

export const checkAndCreateUserPersonalArea = async (user) => {
    try {
        const userDocRef = doc(db, 'users', user.uid);
        const userDoc = await getDoc(userDocRef);

        if (!userDoc.exists()) {
            // יצירת מסמך חדש לאזור אישי אם לא קיים
            await setDoc(userDocRef, {
                email: user.email,
                displayName: user.displayName,
                createdAt: new Date(),
            });

            // יצירת הקולקציות "beforeCheck" ו-"afterCheck" בתוך המסמך של המשתמש
            const beforeCheckRef = doc(collection(userDocRef, 'beforeCheck'));
            await setDoc(beforeCheckRef, {});

            const afterCheckRef = doc(collection(userDocRef, 'afterCheck'));
            await setDoc(afterCheckRef, {});

            console.log("אזור אישי וקולקציות נוצרו למשתמש:", user.uid);
        } else {
            console.log("אזור אישי קיים למשתמש:", user.uid);
        }
    } catch (error) {
        console.error("שגיאה במהלך יצירת אזור אישי:", error);
    }
};

export const savePdfToFirestore = async (emailData, user) => {
    try {
        const userDocRef = doc(db, 'users', user.uid);
        const beforeCheckRef = doc(collection(userDocRef, 'beforeCheck'));

        // שמירת ה-PDF והמידע הנוסף ב-Firestore
        await setDoc(beforeCheckRef, {
            receivedAt: new Date(parseInt(emailData.date)),
            sender: emailData.sender,
            pdfBase64: emailData.pdf, // שמירת ה-PDF כ-Base64
        });

        console.log('קובץ PDF והמידע נשמרו ב-Firestore');
    } catch (error) {
        console.error('שגיאה במהלך שמירת ה-PDF ב-Firestore:', error);
    }
};
