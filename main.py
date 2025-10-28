import cv2
import mediapipe as mp
import math
import winsound



# yüz ayarları
mp_face_mesh=mp.solutions.face_mesh
face_mesh=mp_face_mesh.FaceMesh(
    max_num_faces=1, # algılanacak yüz sayısı
    refine_landmarks=True, # detaylı olması için lazım
    min_detection_confidence=0.5, #algı güven eşiği
    min_tracking_confidence=0.5 # takip güven eşiği
)

mp_drawing=mp.solutions.drawing_utils
drawing_spec=mp_drawing.DrawingSpec(thickness=1,circle_radius=1)
# Kamerayı aç
cap = cv2.VideoCapture(0)

def euclidean_distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def play_alarm():
    # windowsun bip sesini kullandım 
    duration = 800  # milisaniye (0.8 saniye)
    freq = 1000     # Hz (sesin tonu)
    winsound.Beep(freq, duration)

# Başlangıçta


CLOSED_FRAMES = 25  # kaç frame kapalı olursa uyarı vermesini istediğimiz kısım 
left_counter = 0
right_counter = 0
EAR_THRESHOLD = 0.25

while True:
    ret, frame = cap.read()   # Kameradan kare al
    if not ret:
        break
    frame_rbg=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=face_mesh.process(frame_rbg)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            ih, iw, _ = frame.shape
            lm = face_landmarks.landmark
            # göz kordinatlarını hazır şekilde aldım bunlar nerdeyse herkes için standart
            # Sol göz koordinatları
            left_top = (int(lm[159].x*iw), int(lm[159].y*ih))
            left_bottom = (int(lm[145].x*iw), int(lm[145].y*ih))
            left_left = (int(lm[33].x*iw), int(lm[33].y*ih))
            left_right = (int(lm[133].x*iw), int(lm[133].y*ih))

            ear_left = euclidean_distance(left_top, left_bottom) / euclidean_distance(left_left, left_right)

            # Sağ göz koordinatları
            right_top = (int(lm[386].x*iw), int(lm[386].y*ih))
            right_bottom = (int(lm[374].x*iw), int(lm[374].y*ih))
            right_left = (int(lm[362].x*iw), int(lm[362].y*ih))
            right_right = (int(lm[263].x*iw), int(lm[263].y*ih))

            ear_right = euclidean_distance(right_top, right_bottom) / euclidean_distance(right_left, right_right)

            # Sol göz kontrol
            if ear_left < EAR_THRESHOLD:
                left_counter += 1
            else:
                left_counter = 0

            # Sağ göz kontrol
            if ear_right < EAR_THRESHOLD:
                right_counter += 1
            else:
                right_counter = 0


            alarm_played = False
            # Eğer her iki göz de CLOSED_FRAMES kadar kapalıysa uyar
            if left_counter >= CLOSED_FRAMES and right_counter >= CLOSED_FRAMES:
                cv2.putText(frame, "UYKUYA KALDIN!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2) # ekranda uyarının cıkacagı kısım
                if not alarm_played:
                    play_alarm()
                    alarm_played = True
            else:
                alarm_played = False    

            
            
            
            
            mp_drawing.draw_landmarks(
                image=frame,  # o an kullanılacak kare 
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION, # hangi noktaları bir birne bağlayacagını yani yüzün ağını temslil eder
                landmark_drawing_spec=drawing_spec, # noktaları temsil eder
                connection_drawing_spec=drawing_spec # bağlantıları temsil eder
            )    
    
    
    
    
    
    cv2.imshow("Kamera Testi", frame)  # Kameradan gelen kareyi göster

    # ESC tuşuna basınca çık
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
