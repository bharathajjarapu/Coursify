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

def hero_section():
    st.markdown("""
    <style>
    .hero {
        padding: 3rem;
        background-color: #f0f0f0;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 {
        color: #1e3d59;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .hero p {
        color: #333;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
    
    <div class="hero">
        <h1>AI Course Generator</h1>
        <p>Transform any topic into a comprehensive, engaging course outline with just a few clicks!</p>
    </div>
    """, unsafe_allow_html=True)

def generate_course(topic, search_results):
    description = "You are an experienced educator tasked with creating a comprehensive course outline on the given topic."
    instructions = [
        "Create an engaging and informative course outline based on the provided topic and search results.",
        "The course should be structured like a detailed index with basic information for each section.",
        "Include an introduction, learning objectives, 4-5 main modules with 3-5 subtopics each, and a conclusion.",
        "For each concept or topic, provide a brief explanation followed by a relevant YouTube source link to learn.",
        "Ensure the content is substantial, informative, and well-organized, resembling a full course page.",
        "Use markdown formatting to structure the document clearly and try rendering formulaes in md."
    ]
    course_format = """
# {topic}

## Course Overview
[Provide a paragraph overview of the course, its importance, and what students will gain from it.]

## Course Outline

### Module 1: [Module Title]
Explain overview of the module - 2-3 sentences

#### 1.1 [Subtopic 1]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 1.2 [Subtopic 2]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 1.3 [Subtopic 3]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

### Module 2: [Module Title]
Explain overview of the module - 2-3 sentences

#### 2.1 [Subtopic 1]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 2.2 [Subtopic 2]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 2.3 [Subtopic 3]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

### Module 3: [Module Title]
Explain overview of the module - 2-3 sentences

#### 3.1 [Subtopic 1]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 3.2 [Subtopic 2]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 3.3 [Subtopic 3]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

### Module 4: [Module Title]
Explain overview of the module - 2-3 sentences

#### 4.1 [Subtopic 1]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 4.2 [Subtopic 2]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

#### 4.3 [Subtopic 3]
- Point 1: [2-3 sentence explanation of the subtopic]
- Point 2: [2-3 sentence explanation of the subtopic]
- Point 3: [2-3 sentence explanation of the subtopic]
- Point 4:**Formula:** [Insert any relevant formula here if applicable]
- Point 5:**Reference:** [Source Title](link)
- Point 6:**YouTube Link:** [Watch on YouTube](https://www.youtube.com/results?search_query={Subtopic+1+YouTube})

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
    hero_section()
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
