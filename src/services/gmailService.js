/*import { google } from 'googleapis';
import { savePdfToFirestore } from './firestoreService';

const oAuth2Client = new google.auth.OAuth2(
  process.env.REACT_APP_CLIENT_ID,
  process.env.REACT_APP_CLIENT_SECRET,
  process.env.REACT_APP_REDIRECT_URI
);

// פונקציה לקבלת Access Token
export const setCredentials = async (user) => {
    const userTokens = user?.stsTokenManager;
    if (userTokens) {
        oAuth2Client.setCredentials({
            access_token: userTokens.accessToken,
            refresh_token: userTokens.refreshToken,
        });
    } else {
        throw new Error('User tokens not found');
    }
};

export const fetchAndProcessEmails = async (user) => {
    try {
        await setCredentials(user);

        const gmail = google.gmail({ version: 'v1', auth: oAuth2Client });
        const res = await gmail.users.messages.list({
            userId: 'me',
            q: '', // ניתן להוסיף פילטרים לחיפוש לפי הצורך
            maxResults: 100, // מספר האימיילים לטעון
        });

        const messages = res.data.messages || [];
        for (let message of messages) {
            const msg = await gmail.users.messages.get({
                userId: 'me',
                id: message.id,
            });

            const parts = msg.data.payload.parts || [];
            for (let part of parts) {
                if (part.filename && part.filename.endsWith('.pdf')) {
                    const pdfData = await gmail.users.messages.attachments.get({
                        userId: 'me',
                        messageId: message.id,
                        id: part.body.attachmentId,
                    });

                    const pdfContent = pdfData.data.data;
                    const emailData = {
                        date: msg.data.internalDate,
                        sender: msg.data.payload.headers.find(header => header.name === 'From').value,
                        pdf: pdfContent, // קובץ ה-PDF מקודד ב-Base64
                    };

                    await savePdfToFirestore(emailData, user);
                }
            }
        }
    } catch (error) {
        console.error('שגיאה במהלך קריאת או עיבוד האימיילים:', error);
    }
};
*/