import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import Link from 'next/link';
import styles from '../styles/CommentDetector.module.css'

const AppNavbar = () => {
    return (<Navbar bg="dark" variant="dark">
        <Container>
            <Navbar.Brand href="#home">SPOTTY The Bot</Navbar.Brand>
            <Nav className="me-auto">
                <Link href="/comment-detector" className={styles.link}>Spam Detection</Link>
                <Link href="/insta-comment-detector" className={styles.link}>Instagram Detection</Link>
            </Nav>
        </Container>
    </Navbar>)
}

export default AppNavbar;