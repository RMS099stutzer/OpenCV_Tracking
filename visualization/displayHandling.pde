int baseTime1 = 0;
int baseTime2 = 0;

int remainingSeconds = 5;

int loadingStatus;
int loadingIncrement;
int isFinishMessage;
int loadingProgress;
int loadingDotState;

int loadingElapsedTime;
int dotAnimationElapsedTime;
int loadingInterval;

float loadingDot0;
float loadingDot1;
float loadingDot2;

void displayStartScreen() {
    camera(0, 10, 500, 0, 0, 0, 0, 0, -1);
    hint(DISABLE_DEPTH_TEST);
    fill(0);
    textSize(54);
    text("ENTERキーを押して", 0, 0);
    textAlign(CENTER, CENTER);
    hint(ENABLE_DEPTH_TEST);
}

void displayEndScreen() {
    loadingElapsedTime = millis() - baseTime1;
    dotAnimationElapsedTime = millis() - baseTime2;
    camera(0, 10, 500, cameraX, cameraY, 0, 0, 0, -1);
    background(255);
    hint(DISABLE_DEPTH_TEST);
    noFill();
    rect(100, 230, 400, 20);
    if (loadingStatus == 1) {
        fill(0, 0, 255);
        rect(100, 230, loadingProgress, 20);
        if (loadingProgress == 80) {
            loadingInterval = 500;
            loadingIncrement = 40;
        } else if (loadingProgress == 120) {
            loadingIncrement = 120;
        } else if (loadingProgress == 360) {
            loadingIncrement = 36;
        } else if (loadingProgress == 396) {
            loadingInterval = 1000000000;
            isFinishMessage = 1;
            baseTime = millis();
            loadingStatus = 2;
        }
    } else if (loadingStatus == 2) {
        fill(0, 0, 255);
        rect(100, 230, loadingProgress, 20);
    }
    if (loadingElapsedTime > loadingInterval) {
        baseTime1 = millis();
        loadingProgress += loadingIncrement;
        loadingStatus = 1;
    }
    fill(0);
    textSize(30);
    text("送信中", 220, 210);
    text(".", 272, 212 + ( -10 * abs(sin(loadingDot0 + PI))));
    text(".", 292, 212 + ( -10 * abs(sin(loadingDot1 + PI))));
    text(".", 312, 212 + ( -10 * abs(sin(loadingDot2 + PI))));
    if (dotAnimationElapsedTime > 10) {
        if (loadingDotState == 0) {
            loadingDot0 += 0.1;
            baseTime2 = millis();
            if (loadingDot0 >= 3) {
                loadingDot0 = 0;
                loadingDotState = 1;
            }
        } else if (loadingDotState == 1) {
            loadingDot1 += 0.1;
            baseTime2 = millis();
            if (loadingDot1 >= 3) {
                loadingDot1 = 0;
                loadingDotState = 2;
            }
        } else if (loadingDotState == 2) {
            loadingDot2 += 0.1;
            baseTime2 = millis();
            if (loadingDot2 >= 3) {
                loadingDot2 = 0;
                loadingDotState = 0;
            }
        }
    }
    textAlign(LEFT, CENTER);
    text("(" + int(((loadingProgress / 4) * 10.34)) + "/1024)", 320, 210);
    textAlign(CENTER, CENTER);
    textSize(54);
    hint(ENABLE_DEPTH_TEST);
}