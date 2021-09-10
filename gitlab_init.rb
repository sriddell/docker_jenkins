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
    token = u.personal_access_tokens.create(scopes: [:api], name: 'jenkins');
    token.set_token("skfj2348yrhauewsdfisa");
    token.save!
end