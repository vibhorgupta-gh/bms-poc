package com.example.uday_vig.synd;

import android.app.ProgressDialog;

import androidx.annotation.NonNull;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

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
        
        final Context context = getApplicationContext();

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
                    try{
                        RequestQueue requestQueue = Volley.newRequestQueue(SignupActivity.this);
                        String URL = "http://192.168.1.11:5000/otp";
                        JSONObject jsonBody = new JSONObject();
                        jsonBody.put("contact", phone);
                        final String requestBody = jsonBody.toString();

                        StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                Log.i("VOLLEY", response);
                            }
                        }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                Log.e("VOLLEY", error.toString());
                            }
                        }) {
                            @Override
                            public String getBodyContentType() {
                                return "application/json; charset=utf-8";
                            }

                            @Override
                            public byte[] getBody() throws AuthFailureError {
                                try {
                                    return requestBody == null ? null : requestBody.getBytes("utf-8");
                                } catch (UnsupportedEncodingException uee) {
                                    VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s", requestBody, "utf-8");
                                    return null;
                                }
                            }

                            @Override
                            protected Response<String> parseNetworkResponse(NetworkResponse response) {
                                String responseString = "";
                                if (response != null) {
                                    try {
                                        String str = new String(response.data, "UTF-8");
                                        Log.e("YOLO", "parseNetworkResponse: " + str);
                                    } catch (UnsupportedEncodingException e) {
                                        e.printStackTrace();
                                    }
                                }
                                return Response.success(responseString, HttpHeaderParser.parseCacheHeaders(response));
                            }
                        };

                        requestQueue.add(stringRequest);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    androidx.appcompat.app.AlertDialog.Builder builder = new androidx.appcompat.app.AlertDialog.Builder(SignupActivity.this);

                    final EditText input = new EditText(SignupActivity.this);
                    LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                            LinearLayout.LayoutParams.MATCH_PARENT,
                            LinearLayout.LayoutParams.MATCH_PARENT);
                    input.setLayoutParams(lp);
                    builder.setView(input);

                    builder.setCancelable(true);
                    builder.setMessage("Enter OTP");
                    builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            String ip = input.getText().toString().trim();

                            try{
                                RequestQueue requestQueue = Volley.newRequestQueue(SignupActivity.this);
                                String URL = "http://192.168.1.11:5000/check";
                                JSONObject jsonBody = new JSONObject();
                                jsonBody.put("contact", phone);
                                jsonBody.put("otp", ip);
                                final String requestBody = jsonBody.toString();

                                StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                                    @Override
                                    public void onResponse(String response) {
                                        Log.i("VOLLEY", response);
                                    }
                                }, new Response.ErrorListener() {
                                    @Override
                                    public void onErrorResponse(VolleyError error) {
                                        Log.e("VOLLEY", error.toString());
                                    }
                                }) {
                                    @Override
                                    public String getBodyContentType() {
                                        return "application/json; charset=utf-8";
                                    }

                                    @Override
                                    public byte[] getBody() throws AuthFailureError {
                                        try {
                                            return requestBody == null ? null : requestBody.getBytes("utf-8");
                                        } catch (UnsupportedEncodingException uee) {
                                            VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s", requestBody, "utf-8");
                                            return null;
                                        }
                                    }

                                    @Override
                                    protected Response<String> parseNetworkResponse(NetworkResponse response) {
                                        String responseString = "";
                                        if (response != null) {
                                            responseString = new String(response.data);
                                            Log.e(TAG, "parseNetworkResponse: " + responseString);

                                            if(responseString.equals("\"valid\"")){
                                                /*final ProgressDialog progressDialog = ProgressDialog.show(context, "",
                                                        "Creating User...",true);*/

                                                firebaseAuth.createUserWithEmailAndPassword(email, password)
                                                        .addOnSuccessListener(new OnSuccessListener<AuthResult>() {
                                                            @Override
                                                            public void onSuccess(AuthResult authResult) {
                                                                //Successfully created user
                                                                //progressDialog.dismiss();
                                                                firebaseUser = firebaseAuth.getCurrentUser();
                                                                DatabaseReference databaseReference = firebaseDatabase.getReference("users/" + firebaseUser.getUid() + "/");
                                                                User user = new User(firebaseUser.getUid(), name, phone, email, assets);
                                                                databaseReference.setValue(user);

                                                                startActivity(new Intent(context, QRScannerActivity.class));
                                                            }
                                                        }).addOnFailureListener(new OnFailureListener() {
                                                    @Override
                                                    public void onFailure(@NonNull Exception e) {
                                                        //Couldn't create user
                                                        //progressDialog.dismiss();
                                                        /*Toast.makeText(context, "Couldn't create user",
                                                                Toast.LENGTH_SHORT).show();*/

                                                        Log.e(TAG, "onFailure: Couldn't create user" + e.getMessage());
                                                    }
                                                });
                                            }else{
                                                Log.e(TAG, "parseNetworkResponse: Invalid OTP");
                                            }
                                        }
                                        return Response.success(responseString, HttpHeaderParser.parseCacheHeaders(response));
                                    }
                                };

                                requestQueue.add(stringRequest);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    });

                    builder.create();
                    builder.show();
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











                /*if(!name.isEmpty() && !email.isEmpty() && !assets.isEmpty() && !phone.isEmpty() && !password.isEmpty()){
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
                }*/
            }
        });
    }

    @Override
    public void onBackPressed() {

    }
}
