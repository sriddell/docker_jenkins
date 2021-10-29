u = User.find_by_username('root');
tokens = u.personal_access_tokens
found = false
tokens.each do |t|
    if t.name == 'root_token'
        found = true
        break
    end
end
if !found
    token = u.personal_access_tokens.create(scopes: [:api, :read_user, :read_api, :read_repository, :write_repository], name: 'root_token');
    token.set_token("skfj2348yrhauewsdfisa");
    token.save!
end
if !User.exists?(username: ENV['GIT_USER']) then
    u = User.create(username: ENV['GIT_USER'], name:'sriddell', email:'no@none.net',password: ENV['GIT_PASSWORD'], skip_confirmation: true)
    u.save!
end