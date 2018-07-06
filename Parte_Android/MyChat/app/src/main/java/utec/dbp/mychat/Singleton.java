package utec.dbp.mychat;

import android.content.Context;

import com.android.volley.RequestQueue;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

public class Singleton {
    private static Singleton mInstance;
    private RequestQueue mRequestQueue;
    private static Context mContext;

    private Singleton(Context context){
        mContext = context;
        mRequestQueue = getRequestQueue();
    }

    public RequestQueue getRequestQueue() {
        if (mRequestQueue == null){
            mRequestQueue = Volley.newRequestQueue(mContext.getApplicationContext());
        }
        return mRequestQueue;
    }

    public static synchronized Singleton getInstance(Context context){
        if (mInstance == null){
            mInstance =  new Singleton(context);
        }
        return mInstance;
    }

    public <T> void addToRequestQueue(StringRequest req){
        getRequestQueue().add(req);
    }
}
