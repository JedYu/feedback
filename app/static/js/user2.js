

var UserNode = React.createClass({
	render: function() {
		return (
			<li>
			<div class='list-item-name'>{ this.props.item.name }</div>
			<div class='pull-right'>
			<a class="btn btn-sm btn-default" href="/YuJian/cloudeye-android-phone-oem-jxjt/edit" id="edit_project_20">Edit</a>
			<a class="btn btn-sm btn-danger"  rel="nofollow">Destroy</a>
			</div>
			</li>
			);
	}
});

var UserList = React.createClass({
	render: function() {
		var userNodes = this.props.users.map(function (user) {
			return (
				<UserNode user={user}>
				</UserNode>
				);
		});
		return (
			<ul class="well-list">
			{userNodes}
			</ul>
			);
	}
});

var UserBox = React.createClass({
	loadCommentsFromServer: function() {
		$.post("/manager/users", {}, function(data)
		{
			this.setState({users: data});
		});
	},

	getInitialState: function() {
		return {users: []};
	},
	componentDidMount: function() {
		this.loadCommentsFromServer();
	},
	render: function() {
		return (
			<div className="commentBox">
			<h1>Comments</h1>
			<UserList users={this.state.users} />
			</div>
			);
	}
});

