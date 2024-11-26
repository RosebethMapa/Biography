import streamlit as st
import json
import os

BIO_FILE = "biography.json"

DEFAULT_BIO = {
    "name": "Rosebeth L. Mapa",
    "bio": "I'm a dedicated and accomplished individual, recognized for my unwavering commitment to excellence and my ability to inspire those around me through integrity, innovation, and passion for sport (volleyball).",
    "education": [
        {
            "school": "Surigao Del Norte State University",
            "course": "Bachelor of Science in Computer Engineering",
            "year": "1st year"
        }
    ],
    "accomplishments": [
        "- Consistent with Honors in my JHS and SHS days",
        "- Academic Athletes",
        "- Leadership",
        "- Varsity Player (best open spiker)",
        "- Setting as Photo Journalism",
        "- Academic Excellence in STEM Fields"
    ],
    "image": "uploaded_image_462555289_461753836989993_4832604167323898113_n.jpg"
}

def load_bio():
    if os.path.exists(BIO_FILE):
        with open(BIO_FILE, "r") as file:
            return json.load(file)
    return DEFAULT_BIO

def save_bio(data):
    with open(BIO_FILE, "w") as file:
        json.dump(data, file, indent=4)

bio_data = load_bio()

st.title("Biography")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Biography", "Education", "Accomplishments", "Upload Image", "View Biography"])

with tab1:
    st.subheader("Personal Biography")
    name = st.text_input("Name", value=bio_data.get("name", ""))
    bio = st.text_area("Write your biography", value=bio_data.get("bio", ""))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save Biography"):
            bio_data["name"] = name
            bio_data["bio"] = bio
            save_bio(bio_data)
            st.success("Biography saved successfully!")
    with col2:
        if st.button("Change Biography"):
            bio_data["bio"] = bio  
            save_bio(bio_data)
            st.success("Biography updated successfully!")


with tab2:
    st.subheader("Educational Background")
    school = st.text_input("School/University Name")
    course = st.text_input("Course")  
    year = st.text_input("Year")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Add Education"):
            if school and course and year:
                new_education = {"school": school, "course": course, "year": year}
                bio_data["education"].append(new_education)
                save_bio(bio_data)
                st.success("Education added successfully!")
            else:
                st.warning("Please fill out all fields.")
    with col2:
        if st.button("Save Education"):
            save_bio(bio_data)
            st.success("Education data saved successfully!")
    
    st.write("### Education History")
    for i, edu in enumerate(bio_data.get("education", [])):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- {edu['course']} from {edu['school']} ({edu['year']})")
        with col2:
            if st.button("Change", key=f"change_edu_{i}"):
                
                school = edu["school"]
                course = edu["course"]
                year = edu["year"]
                bio_data["education"][i] = {"school": school, "course": course, "year": year}
                save_bio(bio_data)
                st.success("Education updated successfully!")
                st.experimental_rerun()


with tab3:
    st.subheader("Accomplishments")
    accomplishments_text = st.text_area(
        "Add your accomplishments (one per line, starting with '-')", 
        value="\n".join(bio_data.get("accomplishments", []))
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save Accomplishments"):
            bio_data["accomplishments"] = [
                line.strip() for line in accomplishments_text.split("\n") if line.strip()
            ]
            save_bio(bio_data)
            st.success("Accomplishments saved successfully!")
    with col2:
        if st.button("Change Accomplishments"):
            save_bio(bio_data)
            st.success("Accomplishments updated successfully!")

    st.write("### Accomplishments List")
    for acc in bio_data.get("accomplishments", []):
        st.write(f"- {acc}")


with tab4:
    st.subheader("Upload Profile Image")
    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        image_path = f"uploaded_image_{uploaded_image.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        bio_data["image"] = image_path
        save_bio(bio_data)
        st.success("Image uploaded successfully!")
    
    if bio_data.get("image"):
        st.image(bio_data["image"], caption="Uploaded Profile Image")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Remove Image"):
                os.remove(bio_data["image"])
                bio_data["image"] = ""
                save_bio(bio_data)
                st.success("Image removed successfully!")
                st.experimental_rerun()
        with col2:
            if st.button("Change Image"):
                st.info("Upload a new image to replace the current one.")


with tab5:
    st.subheader("Complete Biography")
    col1, col2 = st.columns([1, 2])
    with col1:
        if bio_data.get("image"):
            st.image(bio_data["image"], caption="Profile Image")
        else:
            st.write("No image uploaded.")
    with col2:
        st.write(f"### Name: {bio_data.get('name', '')}")
        st.write(f"### Biography:")
        st.write(bio_data.get("bio", ""))
    
    st.write("### Education:")
    for edu in bio_data.get("education", []):
        st.write(f"- {edu['course']} from {edu['school']} ({edu['year']})")
    
    st.write("### Accomplishments:")
    for acc in bio_data.get("accomplishments", []):
        st.write(f"- {acc}")
    
    st.write("---")
    st.subheader("Download Your Biography")
    bio_json = json.dumps(bio_data, indent=4)
    st.download_button(
        label="Download Biography as JSON",
        data=bio_json,
        file_name="biography.json",
        mime="application/json"
    )
