int isDragging = 0;

void mouseDragged() {
    if (mouseButton == LEFT) {
        if (mouseX - pmouseX >= 0) {
            rotationX = map(mouseX - pmouseX, 0, width, 0, 2 * PI);
        }
        if (mouseX - pmouseX <= 0) {
            rotationX = map(mouseX - pmouseX, -width, 0, -2 * PI, 0);
        }
        rotationX += prevRotationX;
        prevRotationX = rotationX;
        if (mouseY - pmouseY >= 0) {
            rotationZ = map(mouseY - pmouseY, 0, height, 0, 2 * PI);
        }
        if (mouseY - pmouseY <= 0) {
            rotationZ = map(mouseY - pmouseY, -height, 0, -2 * PI, 0);
        }
        rotationZ += prevRotationZ;
        prevRotationZ = rotationZ;
    }
    if (mouseButton == CENTER) {
        cameraX += pmouseY - mouseY;
        cameraY += mouseX - pmouseX;
    }
}

void mouseWheel(MouseEvent e) {
    float mw = e.getCount();
    if (mw == 1) {
        scaleFactor *= 0.9;
    }
    if (mw == -1) {
        scaleFactor *= 1.1;
    }
}

void keyPressed() {
    if (key == ENTER) {
        currentState = 1;
    } else if (key == TAB) {
        if (currentState == 1) {
            baseTime1 = millis();
            baseTime2 = millis();
            currentState = 2;
        }
    } else if (key == ESC) {
        currentState = 3;
    }
}