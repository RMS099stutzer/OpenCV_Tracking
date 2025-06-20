void handleEndScreenState() {
    if (isFinishMessage == 1) {
        if (elapsedTime >= 1000) {
            baseTime = millis();
            remainingSeconds--;
        }
        if (remainingSeconds == 0) {
            stateManager.state = 0;
            stateManager.straightMode = 0;
            for (int k = 0; k < lineCount; k++) {
                start[k] = new PVector(0, 0, 0);
                end[k] = new PVector(0, 0, 0);
            }
            initializeValues();
        }
    }
}

void initializeValues() {
    resetFlags();
    resetRotation();
    resetCamera();
    resetLoading();
    resetFinishMessage();
    strokeWeight(1);
}

void resetFlags() {
    isFirstReceive = 0;
    lineCount = 0;
    receivedLines = 0;
}

void resetRotation() {
    prevRotationX = PI / 6;
    prevRotationZ = PI / 6;
    rotationX = PI / 6;
    rotationZ = PI / 6;
}

void resetCamera() {
    cameraX = 0;
    cameraY = 0;
    scaleFactor = 1.2;
}

void resetLoading() {
    loadingInterval = 50;
    loadingStatus = 0;
    loadingIncrement = 4;
    loadingProgress = 0;
}

void resetFinishMessage() {
    isFinishMessage = 0;
    remainingSeconds = 5;
    loadingDot0 = 0;
    loadingDot1 = 0;
    loadingDot2 = 0;
    loadingDotState = 0;
}

PrintWriter csvFile;

void createCSVFile() {
    csvFile.println(start[0].x + "," + start[0].y + "," + start[0].z);
    csvFile.flush();
    for (int o = 0; o < receivedLines - 1; o++) {
        if (start[o + 1].x == end[o].x && start[o + 1].y == end[o].y && start[o + 1].z == end[o].z) {
            csvFile.println(start[o + 1].x + "," + start[o + 1].y + "," + start[o + 1].z);
            csvFile.flush();
        } else {
            csvFile.println(end[o].x + "," + end[o].y + "," + end[o].z);
            csvFile.println(OUTLIER_VALUE + "," + OUTLIER_VALUE + "," + OUTLIER_VALUE);
            csvFile.println(start[o + 1].x + "," + start[o + 1].y + "," + start[o + 1].z);
            csvFile.flush();
        }
    }
    csvFile.println(end[receivedLines - 1].x + "," + end[receivedLines - 1].y + "," + end[receivedLines - 1].z);
    csvFile.flush();
    csvFile.close();
}