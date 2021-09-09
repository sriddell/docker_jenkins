u = User.find_by_username('root');
token = u.personal_access_tokens.create(scopes: [:api], name: 'jenkins');
token.set_token("skfj2348yrhauewsdfisa");
token.save!