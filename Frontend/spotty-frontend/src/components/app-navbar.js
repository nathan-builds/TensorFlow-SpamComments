import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const AppNavbar = () => {
    return (
        <Navbar bg="dark" variant="dark">
            <Container>
                <Navbar.Brand href="#home">SPOTTY The Bot</Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="#home">Spam Detection</Nav.Link>
                    <Nav.Link href="#features">Instagram Detection</Nav.Link>
                    <Nav.Link href="#pricing">About</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    )
}

export default AppNavbar;