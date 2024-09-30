import cv2
import numpy as np

class ColorROI:
    def __init__(self, window_name, roi_size=(200, 200)):
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

        # ROIのBGRからLABへ変換
        lab_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

        # 各チャンネルごとの最小値と最大値を取得
        l_min, a_min, b_min = np.min(lab_roi, axis=(0, 1))
        l_max, a_max, b_max = np.max(lab_roi, axis=(0, 1))

        # 最小値と最大値を返す
        return start_point, end_point, (l_min, a_min, b_min), (l_max, a_max, b_max)

    def draw_roi(self, frame, start_point, end_point):
        # フレーム上に矩形を描画（青色）
        cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("カメラを開くことができません")
        return

    roi_selector = ColorROI('Frame')

    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームを取得できません")
            break

        # ROIの色範囲と座標を取得
        start_point, end_point, min_lab, max_lab = roi_selector.get_roi_color(frame)

        # ROI領域を描画
        roi_selector.draw_roi(frame, start_point, end_point)

        # 余裕を持たせる
        min_lab = tuple(np.maximum(np.array(min_lab) - 30, 0))
        max_lab = tuple(np.minimum(np.array(max_lab) + 30, 255))

        # LAB範囲を指定フォーマットで表示
        # print(f"TRACKING_THRESHOLDS = {{")
        print(f"    'lower': np.array([{int(min_lab[0])}, {int(min_lab[1])}, {int(min_lab[2])}]),")
        print(f"    'upper': np.array([{int(max_lab[0])}, {int(max_lab[1])}, {int(max_lab[2])}]),")
        # print(f"}}")

        # フレームを表示
        cv2.imshow('Frame', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
