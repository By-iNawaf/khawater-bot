print("📜 Poetry Discord Bot - All rights reserved | Developed by Nawaf 💻")
import discord
from discord.ext import commands
from discord import app_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import random
from datetime import datetime

TOKEN = "HERE" # ← توكن البوت غيرها إلى
GUILD_ID = ID  # ← غيّرها إلى بدون فواصل او اضافات نسخ لصقID السيرفر حقك

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

scheduler = AsyncIOScheduler()
scheduled_job = None
channel_to_send = None
# ----------------- قصائد داخلية -----------------
poems = [
    "في قانون عِزة النفس إذا كان خصمك رخيص لا تُحارِبه",
    "لا طاقه لي للكلام ، ولو كان هناك ما هو أهدأ من الصمت لفعلت .",
    "لا تبالي بمن أبعد نفسه .. بنفسه",
    "الأنسان الطيب تبتليه الدنيا بما لا شأن له به .",
    "مُر الصراحة ، وَلا مُر الإستغفال",
    "أرقى الناس ، أقلهم حديثاً عن الناس",
    "احترامك للناس لا يدل على ضعفك بل يدل على تربيتك",
    "كل شيء له علاج إلا سواد القلب ، وقلة الأصل",
    "تحصنوا ، فهناك أعين ملوثة ، لا تعرف للذكر سبيلاً",
    "لا تصدمني يالله بمن احسنت بهم الظن فقد اكتفيت",
    "الجدران التي تبنيها في حياتك قد تكون هي التي تحميك، أو هي التي تقيدك.",
    "عندما ينهدم جدار، يصبح الطريق أكثر وضوحاً أمامك.",
    "الجدران التي تبنيها حول قلبك، قد تكون هي نفسها التي تمنعك من أن تحب.",
    "الجدران ليست مجرد حجارة، بل هي الحواجز التي نضعها في طريقنا لأسباب لا نعرفها.",
    "بعض الجدران تقف بيننا وبين الآخرين، وبعضها فقط تقف بيننا وبين أنفسنا.",
    "الظروف لا تصنع الرجال، الرجال هم من يصنعون الظروف.",
    "الفشل هو مجرد فرصة للبدء من جديد، ولكن هذه المرة بذكاء أكبر.",
    "أفضل انتقام هو أن تعيش حياة سعيدة.",
    "العقل الفطن يشاهد بصمت، بينما يتحدث الجاهل في كل وقت.",
    "الأفعال أبلغ من الكلمات.",
    "الحب أعمى، والصداقة تشفيه.",
    "من يعرف كيف يسيطر على نفسه، لا يحتاج لسيطرة الآخرين.",
    "الوقت لا ينتظر أحدًا.",
    "من يسعى وراء الحقيقة، لا يضل أبداً.",
    "الشخص الذي لا يفكر في المستقبل يعيش في الماضي.",
    "الكرامة أغلى من المال، فإذا فقدت الكرامة، فقدت كل شيء.",
    "أنت أقوى مما تعتقد.",
    "أحيانًا يكمن السكون في أقوى العواطف.",
    "الحياة قصيرة، لذا عشها بحكمة.",
    "من لا يعرف كيف يقدّر الحياة، لا يمكنه أن يفهم حقيقة الحب.",
    "القدر هو ما تقاومه، والنجاح هو ما تفعله.",
    "الحكمة هي أن تعرف متى تتكلم ومتى تصمت.",
    "الظلام لا يطول، النور دائم في النهاية.",
    "ليس العيش طويلاً هو المهم، بل العيش بكرامة.",
    "الصمت أحيانًا يكون أبلغ من الكلام.",
    "إن كنت تستطيع أن تغير طريقة تفكيرك، ستغير حياتك.",
    "العقل هو سر النجاح، ولكن القلب هو سر الحياة.",
    "إن لم تكن جريئًا بما يكفي لتحقيق أحلامك، فستعيش في ظل الآخرين.",
    "من يسير بحذر سيتجنب الوقوع في الهاوية.",
    "أحسن من كلام الناس أن تفعل ما يرضي قلبك.",
    "الصديق الحقيقي هو من يعرفك كما أنت ويظل يحبك.",
    "كل لحظة هي فرصة جديدة لتبدأ من جديد.",
    "الطيبة لا تتطلب جهدًا، لكن تكلفتها كبيرة.",
    "إذا لم تقاتل من أجل ما تريد، فاعلم أنك ستفقده.",
    "الرغبة في التفوق هي خطوة أولى نحو النجاح.",
    "قوة الإنسان تكمن في تحكمه بمشاعره وأفكاره.",
    "الحياة ليست في العيش، بل في كيفية العيش.",
    "الشجاعة لا تعني غياب الخوف، بل التغلب عليه.",
    "تقدير الذات هو مفتاح النجاح.",
    "الكلمات الطيبة لها قوة لا يمكن أن تُقارن.",
    "من لا يعرف كيف يتسامح، لا يعرف كيف يحب.",
    "الحياة لعبة، لكن اللاعب الذكي يعرف كيف يحقق الفوز.",
    "من يزرع خيرًا، يلقى خيرًا.",
    "الغنى ليس في المال، بل في قلب مليء بالسلام.",
    "الصبر مفتاح الفرج.",
    "المشاكل لا تساوي شيئًا مقارنة بالحلول.",
    "العقل الفعال هو الذي يعرف كيف يستخدم الفرص.",
    "التواضع هو أكبر قوة قد يمتلكها الإنسان.",
    "أنت لم تعش حقًا إذا لم تجرب شيئًا جديدًا.",
    "الآلام التي لا نُعبر عنها هي التي تترك أكبر الأثر.",
    "الأمل هو ما يجعلنا نستمر رغم كل شيء.",
    "الحب لا يُفهم، لكنه يُشعر.",
    "الشخص الذي لا يتعلم من الماضي لا يستطيع العيش في المستقبل.",
    "النجاح هو قدرة الشخص على التعلم من فشله.",
    "إمزح بكل شيء ، إلاّ بأمور الدين وتحدث بكل شيء ، إلاّ بأعراض الناس",
    "لا هتلاقيني ،ولا هتلاقي زيي.",
    "لا تعود لمن خذلك، تذكر ما حدث أخر مرة",
    "أنا مش متأقلم أنا صابر",
    "من يستكثر عليك الوضوح...اتركه",
    "لي قلبٍ يتشرّع إذا دق المطر بابه",
    "من فات قديمه تاه ومن رضى بلقيله عاش",
    "عــــلــى عـينك ي تــاجـر",
    "مالقووش فى الوورد عيب قالوا يا أحمر الخدين",
    "مقدرش ع الحمممار اتششطر ع البردعة",
    "علمناهم الشِحاته سبقونا ع الابواب",
    "لا تكن واقعي فالواقع زبـبالة",
    "ضـع موسيقى , المكان حزين للغاية"
    
]

poem_queue = poems.copy()
random.shuffle(poem_queue)

# ----------------- إرسال الإيمبد -----------------
async def send_poem():
    global channel_to_send, poem_queue
    if not channel_to_send:
        return

    if not poem_queue:
        poem_queue = poems.copy()
        random.shuffle(poem_queue)

    verse = poem_queue.pop(0)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # إنشاء مربع صغير باللون الرمادي حول العنوان
    title = f"```\n THugs | اقتباسات \n```"  # مربّع رمادي اللون يحتوي على اسم الشاعر
    
    # إنشاء الرسالة
    message = f"# ! Nawaf 🏷️ \n\n"  # العنوان
    message += title  # العنوان داخل المربع الرمادي
    message += f"\n```ini\n{verse}\n```"  # القصيدة بلون الأزرق داخل الكودالقصيدة

    message += "\n|| @here ||"  # المنشن بشكل صحيح لظهور إشعار للأعضاء في القناة

    sent_message = await channel_to_send.send(message)
    
    # إضافة رياكشن على الرسالة باستخدام ID الرمز التعبيري
    emoji_id = "1310852555806478396"  # ضع هنا ID الرمز التعبيري الخاص بك
    emoji = discord.PartialEmoji(name="custom_emoji", id=int(emoji_id))  # استخدم اسم الرمز التعبيري و ID الخاص به
    await sent_message.add_reaction(emoji)


# ----------------- أوامر سلاش -----------------
@tree.command(name="setup", description="تحديد القناة ووقت الإرسال", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(channel="القناة اللي ترسل فيها", value="المدة بين كل إرسال (مثلاً: 10m، 2h، 1d)", role="الرول اللي تبيه ينمنشن")
async def setup1(interaction: discord.Interaction, channel: discord.TextChannel, value: str, role: discord.Role):
    global channel_to_send, scheduled_job
    channel_to_send = channel

    units = {'m': 'minutes', 'h': 'hours', 'd': 'days'}
    if value[-1] not in units or not value[:-1].isdigit():
        await interaction.response.send_message("الرجاء استخدام صيغة مثل: 10m أو 1h أو 1d", ephemeral=True)
        return

    interval_kwargs = {units[value[-1]]: int(value[:-1])}

    if scheduled_job:
        scheduled_job.remove()

    scheduled_job = scheduler.add_job(send_poem, IntervalTrigger(**interval_kwargs))
    scheduler.start()
    await interaction.response.send_message(f"تم ضبط الإرسال في {channel.mention} كل {value} مع منشن {role.mention}", ephemeral=True)

@tree.command(name="stop", description="إيقاف الإرسال التلقائي", guild=discord.Object(id=GUILD_ID))
async def stop(interaction: discord.Interaction):
    global scheduled_job
    if scheduled_job:
        scheduled_job.remove()
        scheduled_job = None
        await interaction.response.send_message("تم إيقاف الإرسال التلقائي.", ephemeral=True)
    else:
        await interaction.response.send_message("الإرسال غير مفعل حالياً.", ephemeral=True)

@tree.command(name="test", description="إرسال أقتباس الآن للتجربة", guild=discord.Object(id=GUILD_ID))
async def test(interaction: discord.Interaction):
    global channel_to_send
    if not channel_to_send:
        channel_to_send = interaction.channel
    await send_poem()
    await interaction.response.send_message("تم إرسال أقتباسات للتجربة.", ephemeral=True)

@tree.command(name="help", description="معلومات عن البوت وأوامره", guild=discord.Object(id=GUILD_ID))
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title=" By Nawaf | 🎻 ",
        description="بوت يرسل أقتباسات تلقائيًا أو عند الطلب 💬",
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url="https://i.pinimg.com/736x/c5/e9/6b/c5e96b035873d8a84ce394cc38130c17.jpg")

    embed.add_field(
        name="🛠️ الأوامر المتاحة:",
        value=(
            "➤ `/setup1` – ضبط القناة والتوقيت والرول للمنشن\n"
            "➤ `/stop` – إيقاف الإرسال التلقائي\n"
            "➤ `/test` – إرسال بيت أقتباسات الآن (تجريبي)\n"
            "➤ `/help` – عرض هذه الرسالة المساعدة"
        ),
        inline=False
    )

    embed.add_field(
        name="💡 ملاحظات:",
        value=(
            "- استخدم التوقيت مثل: `10m`, `2h`, `1d`\n"
            "- البوت يرسل في القناة اللي تختارها بعد الإعداد"
        ),
        inline=False
    )

    embed.add_field(
        name="📌 الحقوق:",
        value="كل المحتوى أقتباسات محفوظ لأصحابه\nتم البرمجة بواسطة `Nawaf 💻`",
        inline=False
    )

    embed.add_field(
        name="🌐 تواصل معي:",
        value="[سيرفر الدعم](https://discord.gg/Ay4cqudf9r)",
        inline=False
    )

    embed.set_footer(text="! Nawaf ✨", icon_url="https://i.pinimg.com/736x/c5/e9/6b/c5e96b035873d8a84ce394cc38130c17.jpg")

    await interaction.response.send_message(embed=embed, ephemeral=True)
# ----------------- حدث on_message -----------------
@client.event
async def on_message(message):
    # التأكد من أن الرسالة ليست من البوت نفسه
    if message.author.bot:
        return

    # التأكد من أن الرسالة هي بعد رسالة البوت (التي تحتوي على الاقتباس)
    if channel_to_send and message.channel == channel_to_send:
        # إذا كانت الرسالة بعد اقتباس البوت، يتم حذفها
        try:
            await message.delete()
        except discord.Forbidden:
            print("لم يتمكن البوت من حذف الرسالة بسبب عدم وجود صلاحيات")

    # تأكد من تنفيذ الأوامر بعد الرسالة
    await client.process_commands(message)


# ----------------- عند تشغيل البوت -----------------
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="/By # Nawaf 💻"
    )
    await client.change_presence(status=discord.Status.idle, activity=activity)

    try:
        synced = await client.tree.sync(guild=discord.Object(id=1293075128036364348))
        print(f"✅ Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")


client.run(TOKEN)