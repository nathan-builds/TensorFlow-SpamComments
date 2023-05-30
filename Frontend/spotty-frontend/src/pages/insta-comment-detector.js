import {Button, Container, Form, Row} from "react-bootstrap";
import styles from "@/styles/CommentDetector.module.css";
import ListGroup from "react-bootstrap/ListGroup";
import Image from "next/image";
import {useEffect, useState} from "react";
import AppNavbar from "@/components/app-navbar";
import useWebSocket from "react-use-websocket";


const InstaCommentDetector = () => {
    const [comments, setComments] = useState([])

    const socketUrl = 'ws://127.0.0.1:5000/sub';
    useWebSocket(socketUrl, {
        onOpen: () => console.log('opened'),
        onClose: () => console.log('Socket closing from client'),
        onMessage: (msg) => console.log(processComments(JSON.parse(msg.data))),
        //Will attempt to reconnect on all close events, such as server shutting down
        shouldReconnect: (closeEvent) => true,
    });


    const processComments = (commentsJson) => {
        let result = []
        commentsJson['deleted'].forEach(comment => {
            result.push({msg: comment, isSpam: true})
        })
        commentsJson['not_deleted'].forEach(comment => {
            result.push({msg: comment, isSpam: false})
        })
        setComments([...comments, ...result])
    }


    return (
        <div>
            <AppNavbar></AppNavbar>

            <Container className={styles.instaCommentContainer}>
                <Row>
                    <div className={styles.legend}>

                        <div className={styles.iconContainer}>
                            <div>Spam</div>
                            <Image src={'/remove.png'} alt="image" width="32"
                                   height="32"></Image>
                        </div>

                        <div className={styles.iconContainer}>
                            <div>Not Spam</div>
                            <Image src={'/ham.png'} alt="image" width="32"
                                   height="32"></Image>
                        </div>

                    </div>
                </Row>
                <Row>
                    <div className={styles.activeClassContainer}>
                        <h2 className={styles.activeListeningTitle}>Actively listening for comment moderation...</h2>
                    </div>
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

export default InstaCommentDetector;