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
    stateManager.handleKey(key);
}

class StateManager{
    int state = 0;
    int straightMode = 0; 

    void current(){
        switch (state) {
            case 0:                     //Start screen
                displayStartScreen();
                break;
            case 1:
            case 2:                     //Visualization screen
                setCameraRotation();
                renderLines();
                handleClientMessage();
                break;
            case 3:                     //Exit
                exit();
                break;
            case 5:                     //End screen
                elapsedTime = millis() - baseTime;
                displayEndScreen();
                handleEndScreenState();
                break;
        }
    }

    void handleKey(char key){
        if (key == ENTER) {
            state = 1;
        } else if (key == TAB) {
            if (state == 1) {
                baseTime1 = millis();
                baseTime2 = millis();
                state = 2;
            }
        } else if (key == ESC) {
            state = 3;
        } else if (key == 's' || key == 'S') {
            straightMode = 1;
        } else if (key == 'n' || key == 'N') {
            straightMode = 0;
        } else if (key == DELETE) {
            straightLine.lineDelete();
        }
    }
}