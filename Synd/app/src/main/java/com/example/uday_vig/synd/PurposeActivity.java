package com.example.uday_vig.synd;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
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

public class PurposeActivity extends AppCompatActivity  {

    FirebaseDatabase firebaseDatabase;
    FirebaseAuth firebaseAuth;
    FirebaseUser firebaseUser;

    Spinner purposeSpinner;
    String[] purpose;
    boolean ini = true;

    ArrayList<String> al = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_purpose);

        firebaseDatabase = FirebaseDatabase.getInstance();
        firebaseAuth = FirebaseAuth.getInstance();
        firebaseUser = firebaseAuth.getCurrentUser();

        purposeSpinner = findViewById(R.id.purposeSpinner);

        purpose = getResources().getStringArray(R.array.purpose_array);

        ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(this,
                R.array.purpose_array, R.layout.spinner_item);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        purposeSpinner.setAdapter(adapter);

        purposeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                if(!ini) {
                    int idx = parent.getSelectedItemPosition();
                    final String selected = purpose[idx];

                    if(idx != 0){
                        Log.e("YOLO: PurposeActivity", "onItemSelected: " + idx + " " + selected);

                        DatabaseReference databaseReference = firebaseDatabase.getReference("users/" + firebaseUser.getUid() + "/");
                        databaseReference.addListenerForSingleValueEvent(new ValueEventListener() {
                            @Override
                            public void onDataChange(DataSnapshot dataSnapshot) {
                                User details = dataSnapshot.getValue(User.class);
                                Log.e("YOLO: PurposeActivity", "onDataChange: " + details.email);

                                try {
                                    RequestQueue requestQueue = Volley.newRequestQueue(PurposeActivity.this);
                                    String URL = "http://192.168.1.11:5000/fn/" + details.id;
                                    JSONObject jsonBody = new JSONObject();
                                    jsonBody.put("purpose", selected);
                                    jsonBody.put("priority", details.priority);
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
                                        protected Response<String> parseNetworkResponse(final NetworkResponse response) {
                                            String responseString = "";
                                            if (response != null) {

                                                runOnUiThread(new Runnable() {
                                                    @Override
                                                    public void run() {
                                                        try {
                                                            String str = new String(response.data, "UTF-8");
                                                            Log.e("YOLO: PurposeActivity", "parseNetworkResponse: " + str);
                                                            JSONArray arr = new JSONArray(str);
                                                            for(int i = 0; i < arr.length(); i++){
                                                                try {
                                                                    al.add(arr.getString(i));
                                                                } catch (JSONException e) {
                                                                    e.printStackTrace();
                                                                }
                                                            }

                                                            Intent intent = new Intent(PurposeActivity.this, FunctionsActivity.class);
                                                            //intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                                                            intent.putExtra("PURPOSE", selected);
                                                            intent.putStringArrayListExtra("counter", al);
                                                            Log.e("YOLO: PurposeActivity", "onItemSelected: " + al);
                                                            startActivity(intent);
                                                            finish();
                                                        } catch (UnsupportedEncodingException e) {
                                                            e.printStackTrace();
                                                        } catch (JSONException e) {
                                                            e.printStackTrace();
                                                        }
                                                    }
                                                });
                                            }
                                            return Response.success(responseString, HttpHeaderParser.parseCacheHeaders(response));
                                        }
                                    };

                                    requestQueue.add(stringRequest);
                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }
                            }

                            @Override
                            public void onCancelled(DatabaseError databaseError) {

                            }
                        });
                        Toast.makeText(PurposeActivity.this, selected, Toast.LENGTH_LONG).show();
                    }
                }else{
                    ini = false;
                }

                //finish();
            }

            @Override
            public void onNothingSelected(AdapterView<?> parent) {

            }
        });
    }

    @Override
    public void onBackPressed() {

    }
}
