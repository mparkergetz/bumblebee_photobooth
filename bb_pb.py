#!/usr/bin/env python3
import os
import time
import cv2
from picamera2 import Picamera2

def main(output_dir, preview_res=(800, 600), still_res=(4056, 3040)):
    os.makedirs(output_dir, exist_ok=True)

    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration(
        main={"size": preview_res, "format": "RGB888"}
    )
    still_config = picam2.create_still_configuration(
        main={"size": still_res, "format": "RGB888"}
    )

    win = "Bee Cam Preview"

    try:
        while True:
            picam2.configure(preview_config)
            picam2.start()
            # picam2.set_controls({"AeEnable": True, "AwbEnable": True})
            cv2.namedWindow(win, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            while True:
                frame = picam2.capture_array("main")
                h, w = frame.shape[:2]
                cx, cy = w // 2, h // 2
                crop_w, crop_h = 80, 80
                x1 = cx - crop_w // 2
                y1 = cy - crop_h // 2
                x2 = x1 + crop_w
                y2 = y1 + crop_h
                inset_crop = frame[y1:y2, x1:x2]
                zoomed = cv2.resize(inset_crop, (crop_w * 2, crop_h * 2), interpolation=cv2.INTER_NEAREST)
                frame[10:10 + zoomed.shape[0], 10:10 + zoomed.shape[1]] = zoomed

                text = "Press 'c' to capture, 'q' to quit"
                font = cv2.FONT_HERSHEY_SIMPLEX
                scale, th = 0.6, 1
                (tw, th_), _ = cv2.getTextSize(text, font, scale, th)
                margin = 10
                tx = w - tw - margin
                ty = margin + th_
                cv2.rectangle(frame, (tx-5, margin-5), (w-margin+5, margin+th_+5), (0, 0, 0), cv2.FILLED)
                cv2.putText(frame, text, (tx, ty), font, scale, (255, 255, 255), th, cv2.LINE_AA)
                cv2.imshow(win, frame)
                key = cv2.waitKey(1) & 0xFF

                if key == ord('c'):
                    ts = time.strftime("%Y%m%d-%H%M%S")
                    tmp_path = os.path.join(output_dir, f"tmp_{ts}.jpg")
                    picam2.switch_mode_and_capture_file(still_config, tmp_path)
                    picam2.stop()
                    cv2.destroyWindow(win)

                    snap = cv2.imread(tmp_path)
                    if snap is None:
                        picam2.configure(preview_config)
                        picam2.start()
                        cv2.namedWindow(win, cv2.WINDOW_NORMAL)
                        cv2.setWindowProperty(win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                        continue

                    resize_scale = min(preview_res[0]/snap.shape[1],
                                       preview_res[1]/snap.shape[0], 1.0)
                    disp = cv2.resize(snap, (
                        int(snap.shape[1]*resize_scale),
                        int(snap.shape[0]*resize_scale)
                    ))

                    h, w = disp.shape[:2]
                    cx, cy = w // 2, h // 2
                    crop_w, crop_h = 80, 80
                    x1 = max(cx - crop_w // 2, 0)
                    y1 = max(cy - crop_h // 2, 0)
                    x2 = min(x1 + crop_w, w)
                    y2 = min(y1 + crop_h, h)
                    inset_crop = disp[y1:y2, x1:x2]
                    zoomed = cv2.resize(inset_crop, (crop_w * 2, crop_h * 2), interpolation=cv2.INTER_NEAREST)
                    disp[10:10 + zoomed.shape[0], 10:10 + zoomed.shape[1]] = zoomed

                    overlay_text = "Press 'k' to keep, 'r' to retake, 'q' to quit"
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 0.8
                    thickness = 2
                    (tw, th), _ = cv2.getTextSize(overlay_text, font, font_scale, thickness)
                    x = (disp.shape[1] - tw)//2
                    y = disp.shape[0] - 20
                    cv2.rectangle(disp, (x-10, y-th-10), (x+tw+10, y+10), (0,0,0), cv2.FILLED)
                    cv2.putText(disp, overlay_text, (x, y), font, font_scale, (255,255,255), thickness, cv2.LINE_AA)

                    win2 = "Captured Image"
                    cv2.namedWindow(win2, cv2.WINDOW_NORMAL)
                    cv2.setWindowProperty(win2, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                    cv2.imshow(win2, disp)
                    cv2.waitKey(1)
                    time.sleep(0.1)

                    while True:
                        key2 = cv2.waitKey(0) & 0xFF

                        if key2 == ord('k'):
                            cv2.destroyWindow(win2)
                            time.sleep(0.1)
                            final_name = input("Enter new filename (no extension) or press Enter to keep existing filename:\n> ").strip()
                            if final_name:
                                final_path = os.path.join(output_dir, final_name + ".jpg")
                                os.replace(tmp_path, final_path)
                                print(f"Saved as {final_path}")
                            else:
                                print(f"Kept as {tmp_path}")
                            break

                        elif key2 == ord('r'):
                            os.remove(tmp_path)
                            cv2.destroyWindow(win2)
                            break

                        elif key2 == ord('q') or cv2.getWindowProperty(win2, cv2.WND_PROP_VISIBLE) < 1:
                            os.remove(tmp_path)
                            cv2.destroyAllWindows()
                            picam2.close()
                            return
                    break

                elif key == ord('q'):
                    picam2.stop()
                    cv2.destroyWindow(win)
                    picam2.close()
                    return

    finally:
        picam2.close()
        cv2.destroyAllWindows()
        print("Exiting.")

if __name__ == "__main__":
    main(output_dir="./output")