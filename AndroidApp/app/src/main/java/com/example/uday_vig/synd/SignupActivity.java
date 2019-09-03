package com.example.uday_vig.synd;

import android.app.ProgressDialog;

import androidx.annotation.NonNull;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class SignupActivity extends AppCompatActivity {

    private static final String TAG = "SignupActivity";

    FirebaseAuth firebaseAuth;
    FirebaseUser firebaseUser;
    FirebaseDatabase firebaseDatabase;

    EditText nameEditText, emailEditText, assetsEditText, phoneEditText, passwordEditText;
    FloatingActionButton signUpBtn;
    TextView signUpToLoginTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        firebaseAuth = FirebaseAuth.getInstance();
        firebaseDatabase = FirebaseDatabase.getInstance();

        signUpBtn = findViewById(R.id.btnSignUp);

        signUpToLoginTextView = findViewById(R.id.signupToLoginTextView);

        nameEditText = findViewById(R.id.usernameEditText);
        emailEditText = findViewById(R.id.emailEditText);
        assetsEditText = findViewById(R.id.hniEditText);
        phoneEditText = findViewById(R.id.contactEditText);
        passwordEditText = findViewById(R.id.passwordEditText);

        signUpToLoginTextView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(SignupActivity.this, LoginActivity.class));
            }
        });

        signUpBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String name = nameEditText.getText().toString().trim();
                final String email = emailEditText.getText().toString().trim();
                final String assets = assetsEditText.getText().toString().trim();
                final String phone = phoneEditText.getText().toString().trim();
                final String password = passwordEditText.getText().toString().trim();

                Log.e(TAG, name + " " + email + " " + assets + " " + phone + " " + password);
                if(!name.isEmpty() && !email.isEmpty() && !assets.isEmpty() && !phone.isEmpty() && !password.isEmpty()){
                    final ProgressDialog progressDialog = ProgressDialog.show(SignupActivity.this, "",
                            "Creating User...",true);

                    firebaseAuth.createUserWithEmailAndPassword(email, password)
                            .addOnSuccessListener(new OnSuccessListener<AuthResult>() {
                        @Override
                        public void onSuccess(AuthResult authResult) {
                            //Successfully created user
                            progressDialog.dismiss();
                            firebaseUser = firebaseAuth.getCurrentUser();
                            DatabaseReference databaseReference = firebaseDatabase.getReference("users/" + firebaseUser.getUid() + "/");
                            User user = new User(firebaseUser.getUid(), name, phone, email, assets);
                            databaseReference.setValue(user);

                            startActivity(new Intent(SignupActivity.this, PurposeActivity.class));
                        }
                    }).addOnFailureListener(new OnFailureListener() {
                        @Override
                        public void onFailure(@NonNull Exception e) {
                            //Couldn't create user
                            progressDialog.dismiss();
                            Toast.makeText(SignupActivity.this, "Couldn't create user",
                                    Toast.LENGTH_SHORT).show();
                        }
                    });
                }else{
                    if(name.isEmpty()){
                        nameEditText.setError("Required!");
                    }

                    if(email.isEmpty()){
                        emailEditText.setError("Required!");
                    }

                    if(assets.isEmpty()){
                        assetsEditText.setError("Required!");
                    }

                    if(phone.isEmpty()){
                        phoneEditText.setError("Required!");
                    }

                    if(password.isEmpty()){
                        passwordEditText.setError("Required!");
                    }
                }
            }
        });
    }

    @Override
    public void onBackPressed() {

    }
}
