import {Button, Container, Form, Row} from "react-bootstrap";
import styles from "@/styles/CommentDetector.module.css";
import ListGroup from "react-bootstrap/ListGroup";
import Image from "next/image";
import {useEffect, useState} from "react";
import AppNavbar from "@/components/app-navbar";


const InstaCommentDetector = () => {
    const [comments, setComments] = useState([])


    const processResponse = (res) => {
        console.log(res)
        let result = []
        res['deleted'].forEach(val => result.push({msg: val, isSpam: true}))
        res['not_deleted'].forEach(val => result.push({msg: val, isSpam: false}))
        setComments([...comments, ...result])
    }

    setInterval(() => fetch(`http://localhost:5000/update`)
        .then((res) => res.json())
        .then((response) => processResponse(response))
        .catch(err => console.log(`ERROR FETCHING DATA ${err}`)), 60000)

    return (
        <div>
            <AppNavbar></AppNavbar>
            <Container className={styles.instaCommentContainer}>
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

export default InstaCommentDetector;