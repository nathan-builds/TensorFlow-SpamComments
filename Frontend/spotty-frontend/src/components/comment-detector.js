import {Button, Col, Container, Form, Row} from "react-bootstrap";
import ListGroup from 'react-bootstrap/ListGroup';
import styles from '../styles/CommentDetector.module.css'
import {useState} from 'react'

const CommentDetector = () => {

    const [items, setSearchItems] = useState([])
    const [searchText, setSearchText] = useState("");
    const onSearchHandler = () => {
        setSearchItems([...items, searchText])
    }
    const onSearchTyped = (e) => {
        setSearchText(e.target.value)
    }

    return (<div>
            <Container className={styles.parentContainer}>
                <Row className={styles.searchBar}>
                    <Form className="d-flex">
                        <Form.Control
                            type="search"
                            placeholder="Search"
                            className="me-2"
                            aria-label="Search"
                            value={searchText}
                            onChange={onSearchTyped}

                        />
                        <Button onClick={onSearchHandler}>
                            Search
                        </Button>
                    </Form>
                </Row>
                <Row>
                    <ListGroup>
                        {items.map((idx, item) => {
                            return (<ListGroup.Item key={idx}>item</ListGroup.Item>)
                        })}
                    </ListGroup>
                </Row>
            </Container>
        </div>

    )
}

export default CommentDetector;