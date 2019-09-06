package com.example.uday_vig.synd;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import java.util.List;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class MessageAdapter extends RecyclerView.Adapter<MessageAdapter.MyViewHolder> {

    public List<Message> messagesList;

    public void setMessagesList(List<Message> messagesList) {
        this.messagesList = messagesList;
    }

    public class MyViewHolder extends RecyclerView.ViewHolder{
        public TextView time1, time2, msg1, msg2, sender1, sender2;

        public MyViewHolder (View view){
            super(view);

            time1 = view.findViewById(R.id.text_message_time1);
            time2 = view.findViewById(R.id.text_message_time2);

            msg1 = view.findViewById(R.id.text_message_body1);
            msg2 = view.findViewById(R.id.text_message_body2);

            sender1 = view.findViewById(R.id.text_message_name1);
            sender2 = view.findViewById(R.id.text_message_name2);
        }
    }

    public MessageAdapter(List<Message> messagesList) {
        this.messagesList = messagesList;
    }

    @NonNull
    @Override
    public MyViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View itemView = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_message_recieved, parent, false);

        return new MyViewHolder(itemView);
    }

    @Override
    public void onBindViewHolder(@NonNull MyViewHolder holder, int position) {
        Message message = messagesList.get(position);
        if(message.sentOrReceived){
            holder.msg1.setVisibility(View.GONE);
            holder.time1.setVisibility(View.GONE);
            holder.sender1.setVisibility(View.GONE);

            holder.msg2.setVisibility(View.VISIBLE);
            holder.time2.setVisibility(View.VISIBLE);
            holder.sender2.setVisibility(View.VISIBLE);

            holder.msg2.setText(message.message);
            holder.time2.setText(message.createdAt);
            holder.sender2.setText("You");
        }else{
            holder.msg2.setVisibility(View.GONE);
            holder.time2.setVisibility(View.GONE);
            holder.sender2.setVisibility(View.GONE);

            holder.msg1.setVisibility(View.VISIBLE);
            holder.time1.setVisibility(View.VISIBLE);
            holder.sender1.setVisibility(View.VISIBLE);


            holder.msg1.setText(message.message);
            holder.time1.setText(message.createdAt);
            holder.sender1.setText("Assistant");
        }
    }

    @Override
    public int getItemCount() {
        return messagesList.size();
    }
}
