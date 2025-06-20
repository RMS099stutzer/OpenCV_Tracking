int receivedLines;

void handleClientMessage() {
    elapsedTime = millis() - baseTime;
    Client client = server.available();
    if (client == null) {
        return;
    }
    clientMessage = client.readString();
    String[] messageParts = split(clientMessage, ',');
    if (unhex(messageParts[0]) == 43690) {          //AAAA
        start[lineCount] = new PVector(0, 0, 0);
        isFirstReceive = 0;
        if (lineCount != 0 && stateManager.straightMode == 1) {
            straightLine.straightConversion();
        }
    }
    if (unhex(messageParts[0]) == 65535) {          //FFFF
        if (isFirstReceive == 0) {
            start[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
            isFirstReceive = 1;
            straightLine.startSection = lineCount;
        } else {
            end[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
            start[lineCount + 1] = end[lineCount].copy();
            lineCount++;
            receivedLines++;
        }
        baseTime = millis();
    }
    if (stateManager.state == 2) {
        end[lineCount] = new PVector(int(messageParts[1]), int(messageParts[2]), int(messageParts[3]));
        lineCount++;
        receivedLines++;
        csvFile = createWriter("csv/" + year() + nf(month(), 2) + nf(day(), 2) + nf(hour(), 2) + nf(minute(), 2) + nf(second(), 2) + ".csv");
        createCSVFile();
        stateManager.state = 5;
    }
    remainingSeconds = 5;
}

class StraightLine{
    int startSection;
    int lineNumber;
    PVector startPoint = new PVector(0, 0, 0);
    PVector endPoint = new PVector(0, 0, 0);
    PVector lineSection = new PVector(0, 0, 0);

    void straightConversion(){
        lineNumber = lineCount - 1 - startSection;
        startPoint = start[startSection].copy();
        endPoint = end[lineCount - 1].copy();
        lineSection = (PVector.sub(endPoint, startPoint)).div(lineNumber);
        for (int i = startSection; i < lineCount - 1; i++) {
            end[i] = PVector.add(start[i], lineSection);
            start[i + 1] = PVector.add(start[i], lineSection);
        }
    }

    void lineDelete(){
        for (int i = startSection; i < lineCount - 1; i++) {
            start[i] = new PVector(0, 0, 0);
            end[i] = new PVector(0, 0, 0);
        }
        lineCount = startSection;
    }
}