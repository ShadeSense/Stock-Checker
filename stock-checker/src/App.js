import './App.css';
import Routes from "./Routes";
import 'bootstrap/dist/css/bootstrap.min.css';
import { Nav, Navbar } from 'react-bootstrap';

function App() {
  return (
    <div>
      <Navbar fluid fixed="top" bg="dark" variant="dark">
        <Navbar.Brand href="/">Stock Checker</Navbar.Brand>
        <Nav className="directory">
          <Nav.Link href="/find">Find</Nav.Link>
          <Nav.Link href="/remove">Remove</Nav.Link>
          <Nav.Link href="/display">Display</Nav.Link>
        </Nav>
      </Navbar>
      <Routes />
    </div>
  );
}

export default App;