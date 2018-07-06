package utec.dbp.mychat;

import android.content.Context;
import android.util.Log;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;

import java.util.HashMap;
import java.util.Map;

public class Requests {
    public Context mContext;
    private static final String TAG = "Requests";
    public Requests(Context context){
        mContext = context;
    }

    public interface VolleyCallback {
        void onSuccess (String resp);
        void onFailure (String error);
    }

    public void mensajes(final VolleyCallback callback){
        String url = "http://camilaferno.pythonanywhere.com/carrito-android";
        StringRequest stringRequest = new StringRequest(Request.Method.GET, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.d(TAG, "onResponse: " + response);
                callback.onSuccess(response);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d(TAG, "onErrorResponse: " + error.toString());
                callback.onFailure(error.toString());
            }
        }){
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                HashMap<String, String> headers = new HashMap<>();
                headers.put("User-Agent", "android");
                headers.put("Content-Type", "aplication/x-www-form-urlencoded");
                return headers;
            }

        };
        Singleton.getInstance(mContext).addToRequestQueue(stringRequest);
    }
}
