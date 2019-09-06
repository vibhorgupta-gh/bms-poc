package com.example.uday_vig.synd;

public class Message {
    String message;
    boolean sentOrReceived; //true for sent
    String createdAt;

    public Message(String message, boolean sentOrReceived, String createdAt) {
        this.message = message;
        this.sentOrReceived = sentOrReceived;
        this.createdAt = createdAt;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public boolean isSentOrReceived() {
        return sentOrReceived;
    }

    public void setSentOrReceived(boolean sentOrReceived) {
        this.sentOrReceived = sentOrReceived;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public Message() {

    }
}
