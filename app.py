import os
import streamlit as st
from dotenv import load_dotenv
from tavily import TavilyClient
import google.generativeai as genai

load_dotenv()
tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')
st.set_page_config(page_title="Course Generator", page_icon=":book:")

def search_sources(topic, max_results=5):
    with st.spinner("Searching Web"):
        try:
            tavily_search_results = tavily.search(topic, search_depth="advanced", max_results=max_results)
            return tavily_search_results.get('results', [])
        except Exception as e:
            st.error(f"Error during search: {str(e)}")
            return []

def generate_course(topic, search_results):
    description = "You are an experienced educator tasked with creating a comprehensive course outline on the given topic."
    instructions = [
        "Create an engaging and informative course outline based on the provided topic and search results.",
        "The course should be structured like a detailed index with basic information for each section.",
        "Include an introduction, learning objectives, 4-5 main modules with 3-5 subtopics each, and a conclusion.",
        "For each concept or topic, provide a brief explanation followed by a relevant working links to learn.",
        "Make sure to provide working links only and use youtube links too for chapters that need video attention.",
        "Ensure the content is substantial, informative, and well-organized, resembling a full course page.",
        "Use markdown formatting to structure the document clearly."
    ]
    course_format = """
# Comprehensive Course: {topic}

## Course Overview
[Provide a 2-3 paragraph overview of the course, its importance, and what students will gain from it.]

## Course Outline

### Module 1: [Module Title]
[Brief overview of the module - 2-3 sentences]

#### 1.1 [Subtopic 1]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 1.2 [Subtopic 2]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 1.3 [Subtopic 3]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

### Module 2: [Module Title]
[Brief overview of the module - 2-3 sentences]

#### 2.1 [Subtopic 1]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 2.2 [Subtopic 2]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 2.3 [Subtopic 3]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

### Module 3: [Module Title]
[Brief overview of the module - 2-3 sentences]

#### 3.1 [Subtopic 1]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 3.2 [Subtopic 2]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 3.3 [Subtopic 3]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

### Module 4: [Module Title]
[Brief overview of the module - 2-3 sentences]

#### 4.1 [Subtopic 1]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 4.2 [Subtopic 2]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

#### 4.3 [Subtopic 3]
[2-3 sentence explanation of the subtopic]
**Reference:** [Source Title](link)

## Additional Resources
- [Resource 1]: [Brief description] - [Link]
- [Resource 2]: [Brief description] - [Link]
- [Resource 3]: [Brief description] - [Link]

## Conclusion
[Summarize the key points of the course and suggest next steps or advanced topics for further study.]
"""
    prompt = f"{description}\n\nInstructions:\n" + "\n".join(f"- {instruction}" for instruction in instructions)
    prompt += f"\n\nCourse Format:\n{course_format}\n\nTopic: {topic}\n\nSearch Results:\n"
    for result in search_results:
        prompt += f"- {result['title']}: {result['url']}\n"

    try:
        chat_completion = model.generate_content(prompt)
        return chat_completion.text
    except Exception as e:
        st.error(f"Error generating course: {str(e)}")
        return None

def main():
    st.title(":book: AI Course Generator")
    input_topic = st.text_input("Enter a course topic")
    generate_course_btn = st.button("Generate Course")

    if generate_course_btn and input_topic:
        search_results = search_sources(input_topic)
        if search_results:
            with st.spinner("Generating Course"):
                final_course = generate_course(input_topic, search_results)
                if final_course:
                    st.markdown(final_course)
        else:
            st.warning("No search results found. Please try a different topic.")
    elif generate_course_btn:
        st.warning("Please enter a course topic.")

if __name__ == "__main__":
    main()
