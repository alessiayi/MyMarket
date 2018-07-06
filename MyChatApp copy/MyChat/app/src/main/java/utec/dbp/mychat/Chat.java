package utec.dbp.mychat;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;


public class Chat extends AppCompatActivity {
    RecyclerView mRecyclerView;
    RecyclerView.Adapter mAdapter;
    double counter = 0;
    TextView suma;
    Button btn;
    Requests rq= new Requests(this);
    private static final String TAG = "Chat";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);
        mRecyclerView = findViewById(R.id.main_recycler_view);
        suma = findViewById(R.id.suma);
        btn = findViewById(R.id.button);
        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        cargarProductos();
        btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                cargarProductos();
                Toast.makeText(Chat.this, "Productos refrescados", Toast.LENGTH_SHORT).show();
            }
        });


    }

    void cargarProductos() {
        counter = 0;
        rq.mensajes(new Requests.VolleyCallback() {
            @Override
            public void onSuccess(String resp) {
                Log.d(TAG, "onSuccess: " + resp);
                JSONArray mensajes = null;
                try {
                    mensajes = new JSONArray(resp);
                    Log.d(TAG, "onSuccess: " + mensajes);
                    for (int i =0 ; i < mensajes.length(); i++) {
                        JSONObject producto = mensajes.getJSONObject(i);
                        counter += Double.parseDouble(producto.getString("Precio"));
                        Log.d(TAG, "onSuccess: " + String.valueOf(counter));
                    }
                    suma.setText(String.valueOf(counter));
                    mAdapter = new MyAdapter(mensajes,Chat.this);
                    mRecyclerView.setAdapter(mAdapter);
                } catch (JSONException e) {
                    Log.d(TAG, "onSuccess: EXCEPCION");
                    e.printStackTrace();
                }


            }

            @Override
            public void onFailure(String error) {
                Log.d(TAG, "onFailure: FAIL");
            }
        });
    }
}
