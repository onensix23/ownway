// import logo from './logo.svg';
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";

function App() {

  return (
    <div className="App">
      <div className="container-fluid">
        <div className="row navbar justify-content-center">
          <div className="col-md-7">
            <a href="https://ownway.world">
              <img src="https://ownway-bucket.s3.ap-northeast-2.amazonaws.com/images/OWNWAY%403x.png" width="14%"/>
            </a>
          </div>
        </div>
        <div className="row justify-content-center main-content">
          <div className="col-md-3 col-xs-12 main-content-first">
            <p className="main-content-title">우리가 가는 모든 장소</p>
            <p className="main-content-subtitle">내가 가는 곳 어디든지<br /> 공유하면서 소통해보세요!</p>
            <a href="https://apps.apple.com/kr/app/ownway/id1621267794">
              <img src="https://ownway-bucket.s3.ap-northeast-2.amazonaws.com/images/web_appstore_btn.jpeg" width="40%"/>
            </a>
          </div>
          <div className="col-md-4 col-xs-12 main-content-second">
            <img src="https://ownway-bucket.s3.ap-northeast-2.amazonaws.com/images/ow_+mockup.jpeg" className="main-img"/>
          </div>
        </div>
        <div className="row justify-content-center information-container-top">
          <div className="col-md-10">
            <span className="span-title company-title">원앤식스</span>
          </div>
        </div>
        <div className="row justify-content-center information-container">
          <div className="col-md-10">
            <span className="span-title">대표</span>
            <span className="span-content-title">권윤호</span>

          </div>
        </div>
        <div className="row justify-content-center information-container">
          <div className="col-md-10">
            <span className="span-title">사업자등록번호</span>
            <span className="span-content-title">396-32-00542</span>

          </div>
        </div>
        <div className="row justify-content-center information-container">
          <div className="col-md-10">
            <span className="span-title">주소</span>
            <span className="span-content-title">경기도 군포시 고산로 677번길 12, 1305-802</span>

          </div>
        </div>
        <div className="row justify-content-center information-container">
          <div className="col-md-10">
            <span className="span-title">문의</span>
            <span className="span-content-title">onensix23@gmail.com</span>
          </div>
        </div>
        <div className="row justify-content-end information-container-bottom">
          <div className="col-md-1 terms-container">
            <a href='https://ownway.world/terms/termsofservice'>
              <span className="span-content-terms">서비스이용약관</span>
            </a>
          </div>
          <div className="col-md-1 terms-container">
            <a href='https://ownway.world/terms/privacypolicy'>
              <span className="span-content-terms">개인정보처리방침</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
