from face_recognition import FaceRecognition
from tkinter import *
from PIL import ImageTk, Image
import cv2

class FaceBiometryAccessSystem:
    def __init__(self):
        self.root = Tk()
        self.root.title('Face recognition system access')
        self.app = Frame(self.root, bg='white')
        self.app.grid(columnspan=2)
        self.lmain = Label(self.app)
        self.lmain.grid(columnspan=2)
        self.person_to_recognize = ''
        self.person_entry = Entry(self.root, width=20)
        self.person_entry.grid(row=1, padx=1, pady=1, sticky=E)
        self.person_entry.insert(0, 'Enter your name here...')
        self.confirm_button = Button(self.root, text='Confirm', command=self.save_person, width=10)
        self.confirm_button.grid(row=1, column=1, pady=1, padx=1, sticky=W)
        self.root.bind('<Return>', lambda e: self.save_person())
        self.photo_button = Button(self.root, text='Take a photo', command=self.take_photo, width=16)
        self.photo_button['state'] = 'disabled'
        self.photo_button.grid(row=2, pady=1, padx=1, sticky=E+N)
        self.exit_button = Button(self.root, text='Exit', command=self.close_app, width=10)
        self.exit_button['state'] = 'disabled'
        self.exit_button.grid(row=2, column=1, padx=1, pady=1, sticky=W)
        self.status_label = Label('')
        self.status_label.grid(row=3, columnspan=2, pady=1)

        self.stream_on = True
        self.end_stream = False        
        self.cap = cv2.VideoCapture(0)
        self.face_rec = FaceRecognition()
        self.face_rec.prepare_model()
        self.model_names = self.face_rec.get_names()

    def close_app(self):
        self.stream_on = False
        self.root.destroy()
        self.cap.release()
        cv2.destroyAllWindows()

    def save_person(self):
        person = self.person_entry.get().strip()
        if person in self.model_names:
            self.status_label.config(text='Person found in the database', foreground='green')
            self.person_to_recognize = person
            self.photo_button['state'] = 'normal'
        else:
            self.status_label.config(text='Person not found in the database', foreground='red')
            self.person_to_recognize = ''
            self.person_entry.delete(1.0, 'end')
            self.photo_button['state'] = 'disabled'
        self.root.after(2000, lambda : self.status_label.config(text=''))

    def take_photo(self):
        self.stream_on = False
        cv2.rotate(self.frame, cv2.ROTATE_180)
        recognition_result = self.face_rec.recognise(self.frame)
        if recognition_result != None and str(recognition_result).strip().lower() == str(self.person_to_recognize).strip().lower():
            self.status_label.config(text='Verified')
            self.status_label.configure(foreground='green')
            self.exit_button['state'] = 'normal'
        else:
            self.status_label.config(text='Not verified')
            self.status_label.configure(foreground='red')
        self.root.after(2000, lambda : self.status_label.config(text=''))
        self.stream_on = True

    def video_stream(self):
        if self.stream_on is True:
            _, self.frame = self.cap.read()
            cv2.rotate(self.frame, cv2.ROTATE_180)
            self.root.update_idletasks()
            frame_face_detected, _ = self.face_rec.detect_face_and_crop(self.frame, True)
            if frame_face_detected is not None:
                cv2image = cv2.cvtColor(cv2.resize(frame_face_detected, (int(frame_face_detected.shape[1] * 0.5), int(frame_face_detected.shape[0] * 0.5))), cv2.COLOR_BGR2RGBA)
            else:
                cv2image = cv2.cvtColor(cv2.resize(self.frame, (int(self.frame.shape[1] * 0.5), int(self.frame.shape[0] * 0.5))), cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain.imgtk = imgtk
            self.lmain.configure(image=imgtk)
        self.lmain.after(300, self.video_stream)

    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    access_system = FaceBiometryAccessSystem()
    access_system.video_stream()
    access_system.mainloop()
