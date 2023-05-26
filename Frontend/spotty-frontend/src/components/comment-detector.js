import {Button, Col, Container, Form, Row} from "react-bootstrap";
import ListGroup from 'react-bootstrap/ListGroup';
import styles from '../styles/CommentDetector.module.css'
import {useState} from 'react'
import Image from "next/image";

const CommentDetector = () => {

    const [comments, setComments] = useState([])
    const [commentText, setCommentText] = useState("");


    const processResponse = (res) => {
        setComments([...comments, res])
        //setComments([...comments, {msg: "Hello there world", isSpam: true}])
    }

    const onSearchHandler = () => {

        fetch(`http://localhost:5000/spam?comment=${commentText}`)
            .then((res) => res.json())
            .then((response) => processResponse(response))
            .catch(err => console.log(`ERROR FETCHING DATA ${err}`))

    }
    const onSearchTyped = (e) => {
        setCommentText(e.target.value)
    }

    return (<div>
            <Container className={styles.parentContainer}>
                <Row className={styles.searchBar}>
                    <Form className="d-flex">
                        <Form.Control
                            type="search"
                            placeholder="Enter Comment Text"
                            className="me-2"
                            aria-label="Search"
                            value={commentText}
                            onChange={onSearchTyped}

                        />
                        <Button onClick={onSearchHandler}>
                            Evaluate
                        </Button>
                    </Form>
                </Row>
                <Row className={styles.commentsRow}>
                    <ListGroup>
                        {comments.map((comment, idx) => {
                            return (<ListGroup.Item key={idx}>
                                <div className={styles.commentItem}>
                                    <div>{comment.msg}</div>
                                    <Image src={comment.isSpam ? '/remove.png' : '/ham.png'} alt="image" width="32"
                                           height="32"></Image>
                                </div>
                            </ListGroup.Item>)
                        })}
                    </ListGroup>
                </Row>
            </Container>
        </div>

    )
}

export default CommentDetector;