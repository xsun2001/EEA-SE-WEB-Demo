<template>
    <span>
    <v-navigation-drawer
            app
            v-model="drawer"
    >
        <v-list nav>
            <v-list-item
                    :key="i"
                    :to="item.to"
                    link
                    v-for="(item, i) in list_items"
            >
                <v-list-item-action>
                    <v-icon>{{item.icon}}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                    <v-list-item-title>{{item.text}}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>

    <v-app-bar
            app
            color="indigo"
            dark
    >
        <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
        <v-toolbar-title>THU EEA SA Website Demo</v-toolbar-title>
    </v-app-bar>
</span>
</template>

<script>
    export default {
        name: "Navigation",
        data: () => ({
            drawer: null,
            list_items: [
                {
                    to: "/",
                    icon: "mdi-home",
                    text: "Home",
                },
                {
                    to: "/login",
                    icon: "mdi-login",
                    text: "Login",
                },
                {
                    to: "/sign-up",
                    icon: "mdi-account-plus",
                    text: "Sign Up"
                },
                {
                    to: "/about",
                    icon: "mdi-information",
                    text: "About"
                }
            ],
        })
    }
</script>

<style scoped>

</style>