

var UserNode = React.createClass({displayName: "UserNode",
	render: function() {
		return (
			React.createElement("li", null, 
			React.createElement("div", {className: "list-item-name"},  this.props.user.name), 
			React.createElement("div", {className: "pull-right"}, 
			React.createElement("a", {className: "btn btn-xs btn-default"}, "Edit"), 
			React.createElement("a", {className: "btn btn-xs btn-danger"}, "Destroy")
			)
			)
			);
	}
});

var UserList = React.createClass({displayName: "UserList",
	render: function() {
		var userNodes = this.props.users.map(function (user) {
			return (
				React.createElement(UserNode, {user: user})
				);
		});
		return (
			React.createElement("ul", {className: "well-list"}, 
			userNodes
			)
			);
	}
});

var UserBox = React.createClass({displayName: "UserBox",

	getInitialState: function() {
		return {users: []};
	},
	componentDidMount: function() {
		_this = this;
		$.post("/manage/users", {}, function(data)
		{
			_this.setState({users: data.users});
		});
	},
	render: function() {
		return (
			React.createElement(UserList, {users: this.state.users})
			);
	}
});

