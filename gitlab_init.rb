u = User.find_by_username('root');
tokens = u.personal_access_tokens
found = false
tokens.each do |t|
    if t.name == 'jenkins'
        found = true
        break
    end
end
if !found
    token = u.personal_access_tokens.create(scopes: [:api, :read_user, :read_api, :read_repository, :write_repository], name: 'jenkins');
    token.set_token("skfj2348yrhauewsdfisa");
    token.save!
end