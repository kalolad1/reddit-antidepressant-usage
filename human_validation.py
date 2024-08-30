import random

from reportlab.lib.pagesizes import letter  # type: ignore[import-not-found]
from reportlab.pdfgen import canvas  # type: ignore[import-not-found]
from reportlab.lib.utils import simpleSplit  # type: ignore[import-not-found]


from mongodb_helper import mongodb_client


def select_human_validation_set() -> None:
    # Connect to MongoDB
    db = mongodb_client.online_drug_surveillance_db
    posts_collection = db.posts
    validation_collection = db.human_validation_set

    # Retrieve all post IDs
    post_ids = posts_collection.distinct("post_id")

    # Select 100 random post IDs
    selected_post_ids = random.sample(post_ids, 100)

    # Retrieve the selected posts
    selected_posts = posts_collection.find(
        {"post_id": {"$in": selected_post_ids}},
        {"title": 1, "content": 1, "post_id": 1},
    )

    # Insert the selected posts into the human_validation_set collection
    validation_collection.insert_many(selected_posts)


def wrap_text(
    c: canvas.Canvas,
    text: str,
    x: int,
    y: int,
    max_width: int,
    font_name: str = "Helvetica",
    font_size: int = 12,
) -> int:
    lines = simpleSplit(text, font_name, font_size, max_width)
    for line in lines:
        c.drawString(x, y, line)
        y -= font_size + 2  # Adjust line spacing as needed
    return y


def generate_human_validation_documents() -> None:
    # Connect to MongoDB
    db = mongodb_client.online_drug_surveillance_db
    validation_collection = db.human_validation_set

    # Retrieve all posts from the human_validation_set collection
    posts = validation_collection.find({}, {"title": 1, "content": 1, "post_id": 1})

    # Sort by post ID
    posts = sorted(posts, key=lambda x: x["post_id"])

    # Create a PDF document
    pdf_filename = "human_validation_set.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Set up the document
    c.setFont("Helvetica", 12)
    y_position = height - 40

    for index, post in enumerate(posts):
        if y_position < 500:
            c.showPage()
            y_position = height - 40
            c.setFont("Helvetica", 12)

        # Add post ID
        c.setFont("Helvetica-Bold", 14)
        c.drawString(40, y_position, f"#{index + 1}")
        y_position -= 20

        # Add post title
        c.setFont("Helvetica-Bold", 14)
        y_position = wrap_text(
            c, post["title"], 40, y_position, width - 80, "Helvetica-Bold", 14
        )
        y_position -= 5

        # Add post content
        c.setFont("Helvetica", 12)
        y_position = wrap_text(
            c, post["content"], 40, y_position, width - 80, "Helvetica", 12
        )
        y_position -= 20

        if y_position < 300:
            c.showPage()
            y_position = height - 40
            c.setFont("Helvetica", 12)

        # Add questions
        c.drawString(40, y_position, "1) Age: ____________")
        y_position -= 20

        c.drawString(40, y_position, "2) Gender (please circle):  Male  |  Female  ")
        y_position -= 20

        c.drawString(
            40,
            y_position,
            "3) What is the sentiment of the post? (please circle):  Negative  |  Neutral  |  Positive  ",
        )
        y_position -= 20

        c.drawString(
            40,
            y_position,
            "4) Is the post about a personal experience with an antidepressant? (please circle):  Yes  |  No  ",
        )
        y_position -= 20

        c.drawString(
            40,
            y_position,
            "5) Drug name (if multiple present, chose one): ____________________",
        )
        y_position -= 20

        c.drawString(40, y_position, "6) Duration of treatment (please circle one):")
        y_position -= 20
        c.drawString(40, y_position, "  less than one month  |  one to six months  ")
        y_position -= 20
        c.drawString(40, y_position, "  six to twelve months  |  more than one year  ")
        y_position -= 20

        c.drawString(
            40,
            y_position,
            "7) Medication side effects: ________________________________________________________",
        )
        y_position -= 20

        y_position -= 40

    # Save the PDF document
    c.save()


def main() -> None:
    generate_human_validation_documents()


if __name__ == "__main__":
    main()
