from rest_framework import serializers

from user.models import Team, User


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class CreateTeamSerializer(serializers.Serializer):
    teamID = serializers.CharField(max_length=20, required=True)
    mentor = serializers.CharField(max_length=20, required=False)
    leader = serializers.ModelField(model_field=User._meta.get_field('id'), required=True)
    members = serializers.ListField(child=serializers.CharField(max_length=20), required=False)

    def validate(self, attrs):
        if Team.objects.filter(teamID=attrs['teamID']).exists():
            raise serializers.ValidationError('Team already exists')
        return attrs

    
    # def create(self, validated_data):
    #     team = Team.objects.create(
    #         teamID=validated_data['teamID'],
    #     )
    #     print(team)
    #     return team

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']


class AdminTeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, write_only=True)
    # member_count = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'teamID', 'mentor', 'project', 'members']

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['member_count'] = User.objects.filter(team=instance).count()
    #     return representation

    def create(self, validated_data):
        members_data = validated_data.pop('members')
        team = Team.objects.create(**validated_data)
        for member_data in members_data:
            try:
                member = User.objects.get(email=member_data.get('email', ''))
                member.team = team
                member.save()
            except User.DoesNotExist:
                member = User.objects.create(
                    email=member_data.get('email', ''),
                    name=member_data.get('name', ''),
                    team=team
                )
        return team
    
    def update(self, instance, validated_data):
        if Team.objects.filter(teamID=validated_data['teamID']).exclude(id=instance.id).exists():
            raise serializers.ValidationError('Team already exists')

        # instance.save()

        return instance


__all__ = [
    'TeamSerializer',
    'AdminTeamSerializer'
]
