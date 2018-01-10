import React from 'react'
import './Profile.css'
import Loader from '../../components/Loader/Loader'

class Profile extends React.Component {
  componentWillMount () {
    this.setState({profile: {}})
    const {userProfile, getProfile} = this.props.auth
    if (!userProfile) {
      getProfile((err, profile) => {
        this.setState({profile})
      })
    } else {
      this.setState({profile: userProfile})
    }
  }

  render () {
    if (this.state.profile.nickname) {
      const {profile} = this.state
      return (
        <div className="container">
          <div className="profile-area">
            <h1>{profile.name}</h1>
            <div header="Profile">
              <img src={profile.picture} alt="profile"/>
              <div>
                <div> Nickname</div>
                <h3>{profile.nickname}</h3>
              </div>
              <pre>{JSON.stringify(profile, null, 2)}</pre>
            </div>
          </div>
        </div>
      )
    }
    return (<Loader/>)
  }
}

export default Profile
