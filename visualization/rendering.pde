float rotationX;
float rotationZ;
float prevRotationX, prevRotationZ;
float cameraX, cameraY;
float scaleFactor;
int lineCount;

void setCameraRotation() {
    if (sin(rotationZ) >= 0) {
        camera(500 * cos(rotationX) * sin(rotationZ), 500 * sin(rotationX) * sin(rotationZ), 500 * cos(rotationZ), cameraX, cameraY, 0, 0, 0, -1);
    } else {
        camera(500 * cos(rotationX) * sin(rotationZ), 500 * sin(rotationX) * sin(rotationZ), 500 * cos(rotationZ), cameraX, cameraY, 0, 0, 0, 1);
    }
}

void renderLines() {
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
}


