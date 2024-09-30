import cv2
import numpy as np

class ColorROI:
    def __init__(self, window_name, roi_size=(100, 100)):
        self.window_name = window_name
        self.roi_size = roi_size

    def get_roi_color(self, frame):
        h, w, _ = frame.shape
        roi_w, roi_h = self.roi_size

        # 中央に固定されたROIの左上と右下の座標
        start_point = (w // 2 - roi_w // 2, h // 2 - roi_h // 2)
        end_point = (w // 2 + roi_w // 2, h // 2 + roi_h // 2)

        # ROIを抽出
        roi = frame[start_point[1]:end_point[1], start_point[0]:end_point[0]]

        # ROIの平均的なBGR色を計算
        avg_color = cv2.mean(roi)[:3]  # 最後の値はAlpha値なので省略

        return start_point, end_point, avg_color

    def draw_roi(self, frame, start_point, end_point):
        # フレーム上に矩形を描画（青色）
        cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("カメラを開くことができません")
        return

    roi_selector = ColorROI('Frame')
    hsv_color = []
    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームを取得できません")
            break

        # ROIの色と座標を取得
        start_point, end_point, avg_color = roi_selector.get_roi_color(frame)
        hsv_color = cv2.cvtColor(np.uint8([[avg_color]]), cv2.COLOR_BGR2HSV)[0][0]

        # ROI領域を描画
        roi_selector.draw_roi(frame, start_point, end_point)

        # 平均色を表示
        print(f"ROI内の平均BGR色: {avg_color}")

        # フレームを表示
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
    hsv_lower = hsv_color - 20
    hsv_upper = hsv_color + 20

    #     "lower": np.array([0, 0, 200]),
    #"upper": np.array([180, 20, 255]),

    print(f"    lower: np.array({hsv_lower}),")
    print(f"    upper: np.array({hsv_upper}),")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
