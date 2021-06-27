import './App.css';
import React from 'react'
class App extends React.Component {

  constructor(props) {
    super(props)
    // this.state = { 
    //   baseId: null,
    //   basePath: null,
    //   curImgId: null,
    //   curImgPath: null,
    //   curImgLeft: 300,
    //   curImgTop: 300,
    //   isFirstImage: true,
    //   total: null,
    //   left: null
    //  }

     this.state = { 
       baseId: null,
       basePath: 'static/360.jpg',
       curImgId: null,
       curImgPath: 'static/eyetracker/frame231.png',
       curImgLeft: 404,
       curImgTop: 385,
       isFirstImage: true,
       total: null,
       left: null
      }

  }

  componentDidMount(){
    this.getNextPair()
  }

  getNextPair = () => {
    fetch('./get_img_pair')
      .then(data => data.json())
      .then(data => this.setState({
        basePath: data['basePath'],
        baseId: data['baseId'],
        curImgPath: data['curImgPath'], 
        curImgId: data['curImgId'],
        left: data['left'],
        total: this.state.isFirstImage ? data['left'] : this.state.total,
        isFirstImage: false
      }))
  }

  onMouseMove = ev => {
    this.setState({ curImgLeft: ev.clientX, curImgTop: ev.clientY });
  };

  onMouseDown = ev => {
    fetch('./set_img_pair/' + this.state.baseId + '/' + this.state.curImgId+ '/' + this.state.curImgLeft + '/' + this.state.curImgTop)
    this.getNextPair()
  };

  render () {
    return (
      <div className="App">
        <div id="image-container" style={{width: "1680px", position: 'relative'}} 
              onMouseMove={this.onMouseMove.bind(this)} onMouseDown={this.onMouseDown.bind(this)}>
          <img src={this.state.basePath && this.state.basePath} style={{width: "1680px"}} /> 
          <img src={this.state.curImgPath && this.state.curImgPath}
               style={{ width: 300, height: 300, position: 'absolute', opacity: 0.8,
                        zIndex: 1, top: this.state.curImgTop, transform: `translate(-150px, -150px)`, 
                        left: this.state.curImgLeft}} /> 
        </div>
        <h1>{this.state.left} / {this.state.total}</h1>
      </div>
    );
  }
}

export default App;
