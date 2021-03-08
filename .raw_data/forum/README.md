# Forum Dataset

This directory stores raw data crawled from istio forum with the follow format:

| ID   | SeqID | Title | Category  | Raw Text | Template | Comment      |
| ---- | ----- | ----- | --------- | -------- | -------- | ------------ |
| 0    | 0     | title | g/c/n/s/t | raw      | template | raw+template |
Each line represents a **comment** from a **post**. The **post** is a flow containing multiple comments.

The **ID** identifies the number of post and the sequence ID (**SeqID**) represents the comments sequence inside the post. Note that the first SeqID (**SeqID 0**) is the question of the post.

**Title** is the title of the post.

**Category** has four values: *general*, *config*, *networking*, *security* and *telemetry*. Those values from different topics in forum. They could be considered as pre-set labels, but they might be inaccurate.

**Raw Text** is the comment texts in spite of **Template** contents.

The **Template** may be the template we want to predict. Note that they could be correct or wrong. Post owener my post a wrong template to ask why they are wrong in the template.

**Comment** includes both the raw text and template in the same row, which represents the position information of the template.

