import streamlit as st
import json
from pathlib import Path
from datetime import date

# ---------- Basic setup ----------
st.set_page_config(
    page_title="Take 4 Take Growth Agent",
    page_icon="🎬",
    layout="wide"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

CONTENT_FILE = DATA_DIR / "content_queue.json"

# Create the content queue automatically if it does not exist
if not CONTENT_FILE.exists():
    CONTENT_FILE.write_text("[]")


def load_content():
    with open(CONTENT_FILE, "r") as file:
        return json.load(file)


def save_content(content_items):
    with open(CONTENT_FILE, "w") as file:
        json.dump(content_items, file, indent=2)


# ---------- Header ----------
st.title("🎬 Take 4 Take Growth Agent")
st.caption("Content planning, approval tracking, and YouTube growth management.")

# ---------- Sidebar ----------
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Content Queue", "Upload Package", "Analytics", "Settings"]
)

content_items = load_content()

# ---------- Dashboard ----------
if page == "Dashboard":
    st.header("Channel Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Current Subscribers", "200")

    with col2:
        st.metric("Subscriber Goal", "800")

    with col3:
        st.metric("Subscribers Needed", "600")

    with col4:
        st.metric("Weekly Target", "55")

    st.divider()

    st.subheader("Content Status")

    idea_count = len([item for item in content_items if item["status"] == "Idea"])
    draft_count = len([item for item in content_items if item["status"] == "Draft"])
    approval_count = len(
        [item for item in content_items if item["status"] == "Awaiting Approval"]
    )
    scheduled_count = len(
        [item for item in content_items if item["status"] == "Scheduled"]
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ideas", idea_count)
    col2.metric("Drafts", draft_count)
    col3.metric("Awaiting Approval", approval_count)
    col4.metric("Scheduled", scheduled_count)

    st.divider()

    st.subheader("This Week's Focus")
    st.info(
        "Post 5–7 Shorts and one long-form debate or livestream. "
        "Prioritize content that brings in subscribers, not only views."
    )

# ---------- Content Queue ----------
elif page == "Content Queue":
    st.header("Content Queue")

    with st.form("new_content_form"):
        topic = st.selectbox(
            "Topic Lane",
            ["DC / Marvel", "Anime", "Movies / TV", "Sports", "Other"]
        )

        format_type = st.selectbox(
            "Format",
            ["YouTube Short", "Long-form Video", "Livestream", "Community Post"]
        )

        hook = st.text_input(
            "Hook",
            placeholder="Example: DC fans are wrong about this casting decision."
        )

        working_title = st.text_input(
            "Working Title",
            placeholder="Example: DC Fans Are Judging This Too Early"
        )

        planned_date = st.date_input(
            "Planned Publish Date",
            value=date.today()
        )

        submitted = st.form_submit_button("Add to Content Queue")

        if submitted:
            new_item = {
                "topic": topic,
                "format": format_type,
                "hook": hook,
                "working_title": working_title,
                "planned_date": str(planned_date),
                "status": "Idea"
            }

            content_items.append(new_item)
            save_content(content_items)
            st.success("Content idea added to the queue.")

    st.divider()
    st.subheader("Current Queue")

    if content_items:
        st.dataframe(content_items, use_container_width=True)
    else:
        st.warning("No content ideas yet. Add your first idea above.")

# ---------- Upload Package ----------
elif page == "Upload Package":
    st.header("Upload Package")

    st.warning(
        "Draft mode only — human approval is required before upload or publishing."
    )

    st.subheader("AI Draft Placeholders")

    st.text_input(
        "Primary Title",
        value="DC Fans Are Wrong About This"
    )

    st.text_area(
        "Description",
        value=(
            "Take 4 Take breaks down the latest debate. "
            "Tell us whether you agree in the comments."
        )
    )

    st.text_input(
        "Thumbnail Text",
        value="FANS ARE WRONG?"
    )

    st.text_input(
        "Suggested Hashtags",
        value="#DC #Marvel #Take4Take"
    )

    st.text_input(
        "Playlist",
        value="DC and Marvel Debates"
    )

    st.text_area(
        "Pinned Comment",
        value="Is this take correct, or are we completely wrong? Let us know."
    )

    if st.button("Mark as Ready for Human Approval"):
        st.success("Draft package marked for review. No video has been uploaded.")

# ---------- Analytics ----------
elif page == "Analytics":
    st.header("Analytics")

    st.info("This is a placeholder dashboard. YouTube Analytics will be connected later.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Views This Week", "0")
    col2.metric("Watch Time", "0 hours")
    col3.metric("Subscribers Gained", "0")

    st.subheader("Weekly Recommendation")
    st.write(
        "Once YouTube Analytics is connected, this section will identify which "
        "Shorts, topics, titles, and debates bring in the most subscribers."
    )

# ---------- Settings ----------
elif page == "Settings":
    st.header("Take 4 Take Settings")

    st.text_input("Channel Name", value="Take 4 Take Network")

    st.selectbox(
        "Primary Content Lane",
        ["DC / Marvel / Anime / Movies", "Sports", "Hybrid"]
    )

    st.text_area(
        "Channel Promise",
        value=(
            "Unfiltered DC, Marvel, anime, and movie debates "
            "for fans who want real takes."
        )
    )

    st.text_area(
        "Tone Rules",
        value=(
            "Confident, funny, direct, debate-driven, and respectful. "
            "No personal attacks, false claims, or misleading titles."
        )
    )

    st.success(
        "Settings are currently display-only. Save functionality can be added next."
    )
