from django.shortcuts import render
from .forms import ImageUploadForm
from PIL import Image
import cv2
import os
import numpy as np

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img_obj = form.save()

            # Form değerlerini al
            low_h = form.cleaned_data['low_h']
            low_v = form.cleaned_data['low_v']
            low_s = form.cleaned_data['low_s']

            high_h = form.cleaned_data['high_h']
            high_v = form.cleaned_data['high_v']
            high_s = form.cleaned_data['high_s']

            # Load the photo
            img = cv2.imread(img_obj.image.path)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_white = np.array([low_h, low_v, low_s])
            upper_white = np.array([high_h, high_v, high_s])
            mask = cv2.inRange(hsv, lower_white, upper_white)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            filtered_contours = []
            for contour in contours:
                area = cv2.contourArea(contour)
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h
                if area > 100 and aspect_ratio > 0.8 and aspect_ratio < 1.2:
                    filtered_contours.append(contour)

            x_min, y_min, x_max, y_max = img.shape[1], img.shape[0], 0, 0
            for contour in filtered_contours:
                (x, y), radius = cv2.minEnclosingCircle(contour)
                center = (int(x), int(y))
                radius = int(radius)
                cv2.circle(img, center, radius, (215, 9, 255), 2)
                x, y, w, h = cv2.boundingRect(contour)

            # Resmi kaydet
            cv2.imwrite(img_obj.image.path, img)

            return render(request, 'display_image.html', {'img_obj': img_obj})
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})
