package com.example.uday_vig.synd;

public class User {
    String id;
    String name;
    String phone;
    String email;
    int priority;

    public User(String id, String name, String phone, String email, String assets) {
        this.id = id;
        this.name = name;
        this.phone = phone;
        this.email = email;
        this.priority = (Long.valueOf(assets) >= 100) ? 0 : 1;
    }

    public User() {
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getPriority() {
        return priority;
    }

    public void setPriority(int priority) {
        this.priority = priority;
    }
}
