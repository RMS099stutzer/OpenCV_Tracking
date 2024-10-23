import processing.net.*;
import javax.swing.JOptionPane;
import java.awt.Point;

int port = 10001;
Server server;

int baseTime = 0;
int baseTime1 = 0;
int baseTime2 = 0;

int MAX_LINES = 10000;
int lineCount;
PVector[] start = new PVector[MAX_LINES];
PVector[] end = new PVector[MAX_LINES];
int receivedLines;
float rotationX;
float rotationZ;
float prevRotationX, prevRotationZ;
float cameraX, cameraY;
float scaleFactor;
PrintWriter csvFile;
int outlierValue = 9999;
int isFirstReceive = 0;
int remainingSeconds = 2;
int currentState = 0;
int elapsedTime;
int loadingElapsedTime;
int dotAnimationElapsedTime;
int loadingInterval;
String clientMessage;
int repeatCount;
int isDragging = 0;
int loadingStatus;
int loadingIncrement;
int isFinishMessage;
int loadingProgress;
float loadingDot0;
float loadingDot1;
float loadingDot2;
int loadingDotState;
int isFinished;

void setup() {
    fullScreen(P3D);
    stroke(0);
    hint(ENABLE_DEPTH_SORT);
    lights();
    textSize(54);
    frameRate(60);
    server = new Server(this, port);
    println("server address: " + server.ip());
    initializeValues();
    repeatCount = 0;
    textFont(createFont("ＭＳ ゴシック", 48, true));
}

void draw() {
    background(255);
    translate(width / 2, height / 2, 0);
    if (currentState == 3) {
        exit();
    } else if (currentState == 5) {
        elapsedTime = millis() - baseTime;
        displayEndScreen1();
        if (isFinishMessage == 1) {
            if (elapsedTime >= 1000) {
                baseTime = millis();
                remainingSeconds--;
            }
            if (remainingSeconds == 0) {
                currentState = 0;
                for (int k = 0; k < lineCount; k++) {
                    start[k] = new PVector(0, 0, 0);
                    end[k] = new PVector(0, 0, 0);
                }
                initializeValues();
            }
        }
    } else if (currentState == 1 || currentState == 2) {
        if (sin(rotationZ) >= 0) {
            camera(500 * cos(rotationX) * sin(rotationZ), 500 * sin(rotationX) * sin(rotationZ), 500 * cos(rotationZ), cameraX, cameraY, 0, 0, 0, -1);
        } else {
            camera(500 * cos(rotationX) * sin(rotationZ), 500 * sin(rotationX) * sin(rotationZ), 500 * cos(rotationZ), cameraX, cameraY, 0, 0, 0, 1);
        }
        stroke(0);
        rotateX(0);
        rotateY(0);
        scale(scaleFactor);
        textAlign(CENTER);
        text("X", 200, 0, 0);
        text("Y", 0, 200, 0);
        text("Z", 0, 0, 200);
        strokeWeight(1);
        line(0, 0, 0, 160, 0, 0);
        line(0, 0, 0, 0, 160, 0);
        line(0, 0, 0, 0, 0, 160);
        strokeCap(ROUND);
        strokeWeight(10);
        for (int k = 0; k < lineCount; k++) {
            stroke(0);
            strokeWeight(10);
            line(start[k].x, start[k].y, start[k].z, end[k].x, end[k].y, end[k].z);
        }
        elapsedTime = millis() - baseTime;
        Client client = server.available();
        if (client == null) {
            return;
        }
        clientMessage = client.readString();
        String[] messageParts = split(clientMessage, ',');
        if (unhex(messageParts[0]) == 43690) {
            start[lineCount] = new PVector(0, 0, 0);
            isFirstReceive = 0;
        }
        if (unhex(messageParts[0]) == 65535) {
            if (isFirstReceive == 0) {
                start[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
                isFirstReceive = 1;
            } else {
                end[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
                start[lineCount + 1] = end[lineCount];
                lineCount++;
                receivedLines++;
            }
            baseTime = millis();
        }
        if (currentState == 2) {
            end[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
            lineCount++;
            receivedLines++;
            csvFile = createWriter("csv/test_" + repeatCount + ".csv");
            createCSVFile();
            currentState = 5;
            repeatCount++;
        }
        remainingSeconds = 5;
    } else if (currentState == 0) {
        displayStartScreen();
    }
}

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
            isFinished = 1;
            currentState = 2;
        }
    } else if (key == ESC) {
        currentState = 3;
    }
}

void initializeValues() {
    isFirstReceive = 0;
    lineCount = 0;
    receivedLines = 0;
    prevRotationX = PI / 6;
    prevRotationZ = PI / 6;
    rotationX = PI / 6;
    rotationZ = PI / 6;
    cameraX = 0;
    cameraY = 0;
    scaleFactor = 1.2;
    loadingInterval = 50;
    loadingStatus = 0;
    loadingIncrement = 4;
    loadingProgress = 0;
    isFinishMessage = 0;
    remainingSeconds = 2;
    loadingDot0 = 0;
    loadingDot1 = 0;
    loadingDot2 = 0;
    loadingDotState = 0;
    isFinished = 0;
    strokeWeight(1);
}

void createCSVFile() {
    csvFile.println(start[0].x + "," + start[0].y + "," + start[0].z);
    csvFile.flush();
    for (int o = 0; o < receivedLines - 1; o++) {
        if (start[o + 1].x == end[o].x && start[o + 1].y == end[o].y && start[o + 1].z == end[o].z) {
            csvFile.println(start[o + 1].x + "," + start[o + 1].y + "," + start[o + 1].z);
            csvFile.flush();
        } else {
            csvFile.println(end[o].x + "," + end[o].y + "," + end[o].z);
            csvFile.println(outlierValue + "," + outlierValue + "," + outlierValue);
            csvFile.println(start[o + 1].x + "," + start[o + 1].y + "," + start[o + 1].z);
            csvFile.flush();
        }
    }
    csvFile.println(end[receivedLines - 1].x + "," + end[receivedLines - 1].y + "," + end[receivedLines - 1].z);
    csvFile.flush();
    csvFile.close();
}

void displayStartScreen() {
    camera(0, 10, 500, 0, 0, 0, 0, 0, -1);
    hint(DISABLE_DEPTH_TEST);
    fill(0);
    textSize(54);
    text("ENTERキーを押して", 0, 0);
    textAlign(CENTER, CENTER);
    hint(ENABLE_DEPTH_TEST);
}

void displayEndScreen1() {
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