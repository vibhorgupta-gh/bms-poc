package com.example.uday_vig.synd;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

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
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;

public class CounterActivity extends AppCompatActivity {

    FirebaseDatabase firebaseDatabase;
    FirebaseAuth firebaseAuth;
    FirebaseUser firebaseUser;

    TextView currCounterTextView, queueTextView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_counter);

        firebaseDatabase = FirebaseDatabase.getInstance();
        firebaseAuth = FirebaseAuth.getInstance();
        firebaseUser = firebaseAuth.getCurrentUser();

        currCounterTextView = findViewById(R.id.currCounterTextView);
        queueTextView = findViewById(R.id.queueTextView);

        final String purpose = getIntent().getExtras().getString("PURPOSE");
        final ArrayList<String> functions = getIntent().getExtras().getStringArrayList("counters");

        currCounterTextView.append(functions.get(1));
        queueTextView.append(functions.get(2));

        final Handler handler = new Handler();
        final int delay = 2000;

        final DatabaseReference databaseReference = firebaseDatabase.getReference("users/" + firebaseUser.getUid() + "/");
        databaseReference.child("counter").setValue(functions.get(1));
        databaseReference.child("index").setValue(functions.get(2));

         handler.postDelayed(new Runnable() {
             @Override
             public void run() {
                 try {
                     RequestQueue requestQueue = Volley.newRequestQueue(CounterActivity.this);
                     String URL = "http://192.168.43.50:5000/poll";

                     JSONObject jsonBody = new JSONObject();
                     jsonBody.put("uid", firebaseUser.getUid());
                     /*jsonBody.put("counter", functions.get(1));
                     jsonBody.put("index", functions.get(2));*/
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
                                     //Log.e("YOLO", "parseNetworkResponse: " + str);
                                     JSONArray arr = new JSONArray(str);
                                     final String recCounter = arr.getString(1);
                                     final String recIndex = arr.getString(2);

                                     Log.e("YOLO", "parseNetworkResponse: " + recCounter + " " + recIndex);
                                     final DatabaseReference databaseReference = firebaseDatabase.getReference("users/" + firebaseUser.getUid() + "/");
                                     databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
                                         @Override
                                         public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                                             String counter = dataSnapshot.child("counter").getValue(String.class);
                                             String index = dataSnapshot.child("index").getValue(String.class);

                                             if(!counter.equals(recCounter)){
                                                 runOnUiThread(new Runnable() {
                                                     @Override
                                                     public void run() {
                                                         currCounterTextView.setText("You are currently at counter: " + recCounter);
                                                         queueTextView.setText("Please proceed to queue number: " + recIndex);
                                                     }
                                                 });

                                                 databaseReference.child("counter").setValue(recCounter);
                                                 databaseReference.child("index").setValue(recIndex);
                                             }
                                         }

                                         @Override
                                         public void onCancelled(@NonNull DatabaseError databaseError) {

                                         }
                                     });
                                 } catch (UnsupportedEncodingException e) {
                                     Log.e("YOLO", "parseNetworkResponse: " + e.getMessage());
                                 } catch (JSONException e) {
                                     Log.e("YOLO", "parseNetworkResponse: " + e.getMessage());
                                 }
                             }
                             return Response.success(responseString, HttpHeaderParser.parseCacheHeaders(response));
                         }
                     };

                     requestQueue.add(stringRequest);
                 } catch (JSONException e) {
                     e.printStackTrace();
                 }

                 handler.postDelayed(this, delay);
             }
         }, delay);
    }
}
